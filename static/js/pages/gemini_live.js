/**
 * Gemini Live API Client for Mangatarem Cultural Map
 * Handles WebSocket connection, audio streaming (WebRTC), and Function Calling (Map interaction)
 */

class GeminiLiveClient {
    constructor() {
        this.socket = null;
        this.apiKey = null;
        this.systemContext = "";
        
        // Audio handling
        this.audioContext = null;
        this.mediaStream = null;
        this.processor = null;
        this.outputAudioQueue = [];
        this.isPlaying = false;
        
        // State
        this.isConnected = false;
        this.isConnecting = false;
        this.setupComplete = false;
        
        // UI Elements
        this.micButton = document.getElementById('gemini-mic-btn');
        this.statusText = document.getElementById('gemini-status');
        
        if (this.micButton) {
            this.micButton.addEventListener('click', () => this.toggleConnection());
        }
    }

    async toggleConnection() {
        if (this.isConnected || this.isConnecting) {
            this.disconnect();
        } else {
            await this.connect();
        }
    }

    async fetchCredentials() {
        try {
            // Fetch API Key from backend
            const configRes = await fetch('/api/gemini/config');
            const configData = await configRes.json();
            if (configData.api_key) {
                this.apiKey = configData.api_key;
            } else {
                throw new Error("Failed to load Gemini API key");
            }

            // Fetch System Instructions/Context from backend
            const contextRes = await fetch('/api/gemini/context');
            const contextData = await contextRes.json();
            if (contextData.system_instruction) {
                this.systemContext = contextData.system_instruction;
            }
        } catch (error) {
            console.error("Credentials error:", error);
            alert("Could not initialize Live Guide. Please check server configuration.");
            throw error;
        }
    }

    async connect() {
        if (this.isConnecting) return;
        this.isConnecting = true;
        this.setupComplete = false;
        this.updateStatus("Connecting...");
        
        if (!this.apiKey) {
            await this.fetchCredentials();
        }

        const wsUrl = `wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key=${this.apiKey}`;
        this.socket = new WebSocket(wsUrl);

        this.socket.onopen = async () => {
            console.log("Gemini Live WebSocket Connected");
            this.isConnecting = false;
            this.isConnected = true;
            this.updateStatus("Setting up Live Guide...");
            if (this.micButton) this.micButton.classList.add('recording-active');
            
            // Send Setup message with tools and context
            this.sendSetupMessage();
            
            // Start capturing and streaming microphone audio
            await this.startAudioCapture();
        };

        this.socket.onmessage = async (event) => {
            let data;
            if (event.data instanceof Blob) {
                // Read blob as text for JSON parsing
                const text = await event.data.text();
                data = JSON.parse(text);
            } else {
                data = JSON.parse(event.data);
            }
            
            // Log raw messages to catch setup errors or exceptions sent before disconnect
            console.log("Gemini Live message received:", data);
            
            this.handleServerMessage(data);
        };

        this.socket.onclose = (event) => {
            console.warn(`Gemini Live WebSocket Disconnected. Code: ${event.code}, Reason: ${event.reason || 'No reason provided'}`);
            if (event.code !== 1000 && event.code !== 1005) {
                console.error("The API key might be invalid, or the Live API is not enabled for this key.");
            }
            this.disconnect();
        };

        this.socket.onerror = (error) => {
            console.error("Gemini Live WebSocket Error:", error);
            this.disconnect();
        };
    }

    sendSetupMessage() {
        const setupMessage = {
            "setup": {
                "model": "models/gemini-3.1-flash-live-preview",
                "generationConfig": {
                    "responseModalities": ["AUDIO"]
                },
                "systemInstruction": {
                    "parts": [{"text": this.systemContext}]
                },
                "tools": [{
                    "functionDeclarations": [
                        {
                            "name": "pan_map",
                            "description": "Pan the map to specific latitude and longitude coordinates.",
                            "parameters": {
                                "type": "OBJECT",
                                "properties": {
                                    "lat": { "type": "NUMBER", "description": "Latitude" },
                                    "lng": { "type": "NUMBER", "description": "Longitude" }
                                },
                                "required": ["lat", "lng"]
                            }
                        }
                    ]
                }]
            }
        };
        this.socket.send(JSON.stringify(setupMessage));
    }

    async startAudioCapture() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
            this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            if (!this.audioContext) {
                console.warn("AudioContext was destroyed while waiting for mic access. Aborting.");
                return;
            }

            const source = this.audioContext.createMediaStreamSource(this.mediaStream);
            this.processor = this.audioContext.createScriptProcessor(4096, 1, 1);
            
            source.connect(this.processor);
            this.processor.connect(this.audioContext.destination);
            
            this.processor.onaudioprocess = (e) => {
                if (!this.isConnected || this.socket.readyState !== WebSocket.OPEN) return;
                // DO NOT SEND AUDIO UNTIL SETUP IS COMPLETE
                if (!this.setupComplete) return;
                
                // Get raw float32 PCM data
                const channelData = e.inputBuffer.getChannelData(0);
                
                // Convert float32 to int16
                const pcm16 = new Int16Array(channelData.length);
                for (let i = 0; i < channelData.length; i++) {
                    let s = Math.max(-1, Math.min(1, channelData[i]));
                    pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
                }
                
                // Convert int16 to Base64
                const base64Audio = this.bufferToBase64(pcm16.buffer);
                
                const message = {
                    "clientContent": {
                        "turns": [{
                            "role": "user",
                            "parts": [{
                                "inlineData": {
                                    "mimeType": "audio/pcm;rate=16000",
                                    "data": base64Audio
                                }
                            }]
                        }],
                        "turnComplete": true
                    }
                };
                
                this.socket.send(JSON.stringify(message));
            };
        } catch (error) {
            console.error("Audio capture error:", error);
            this.updateStatus("Microphone access denied.");
            this.disconnect();
        }
    }

    handleServerMessage(data) {
        // Handle Setup Complete
        if (data.setupComplete) {
            console.log("Setup complete received from Gemini!");
            this.setupComplete = true;
            this.updateStatus("Connected! Say hi.");
            return;
        }

        // Handle Server Content (Audio)
        if (data.serverContent && data.serverContent.modelTurn) {
            const parts = data.serverContent.modelTurn.parts;
            for (let part of parts) {
                if (part.inlineData && part.inlineData.mimeType.startsWith("audio/pcm")) {
                    this.playAudio(part.inlineData.data);
                }
            }
        }

        // Handle Function Calls (Tools)
        if (data.toolCall && data.toolCall.functionCalls) {
            for (let call of data.toolCall.functionCalls) {
                this.handleFunctionCall(call.name, call.args, call.id);
            }
        }
    }

    handleFunctionCall(name, args, callId) {
        console.log(`Gemini called function: ${name} with args:`, args);
        
        if (name === "pan_map") {
            // Check if our map script has exposed a flyTo or panMap function
            if (typeof window.geminiPanMap === 'function') {
                window.geminiPanMap(args.lat, args.lng);
            } else {
                console.warn("window.geminiPanMap is not defined.");
            }
        }

        // Send function response back to Gemini so it knows we executed it
        const responseMessage = {
            "toolResponse": {
                "functionResponses": [{
                    "id": callId,
                    "response": {
                        "result": "Map panned successfully"
                    }
                }]
            }
        };
        this.socket.send(JSON.stringify(responseMessage));
    }

    // --- Audio Playback Helpers ---
    
    async playAudio(base64Data) {
        // Convert Base64 back to Int16Array, then to Float32Array for AudioBuffer
        const binaryString = atob(base64Data);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        
        const int16Array = new Int16Array(bytes.buffer);
        const float32Array = new Float32Array(int16Array.length);
        for (let i = 0; i < int16Array.length; i++) {
            float32Array[i] = int16Array[i] / 32768.0;
        }

        if (!this.audioContext) return;
        
        const audioBuffer = this.audioContext.createBuffer(1, float32Array.length, 24000); // Gemini output is typically 24kHz
        audioBuffer.getChannelData(0).set(float32Array);
        
        const source = this.audioContext.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(this.audioContext.destination);
        source.start();
    }

    bufferToBase64(buffer) {
        let binary = '';
        const bytes = new Uint8Array(buffer);
        const len = bytes.byteLength;
        for (let i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return window.btoa(binary);
    }

    updateStatus(msg) {
        if (this.statusText) {
            this.statusText.textContent = msg;
        }
    }

    disconnect() {
        this.isConnected = false;
        this.isConnecting = false;
        this.updateStatus("Disconnected.");
        
        if (this.micButton) this.micButton.classList.remove('recording-active');
        
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
        if (this.processor) {
            this.processor.disconnect();
            this.processor = null;
        }
        if (this.mediaStream) {
            this.mediaStream.getTracks().forEach(track => track.stop());
            this.mediaStream = null;
        }
        if (this.audioContext) {
            this.audioContext.close();
            this.audioContext = null;
        }
    }
}

// Initialize on DOM load
document.addEventListener("DOMContentLoaded", () => {
    window.geminiLive = new GeminiLiveClient();
});
