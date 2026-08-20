"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2, ArrowLeft, Send, MessageSquare } from "lucide-react";

interface ChatMessageItem {
  id: number | string;
  sender_id?: number | string | null;
  sender_name?: string;
  content: string;
  created_at?: string | null;
  is_system_msg?: boolean;
}

interface RoomInfo {
  id: string | number;
  name?: string;
  title?: string;
  description?: string;
}

export default function ChatRoomPage() {
  const params = useParams();
  const rawRoom = params.room;
  const roomId = Array.isArray(rawRoom) ? rawRoom[0] : rawRoom;
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  const [room, setRoom] = useState<RoomInfo | null>(null);
  const [messages, setMessages] = useState<ChatMessageItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);

  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!authLoading && !user) router.push("/auth/login");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || !roomId) return;
    const id = Number(roomId);
    setLoading(true);
    Promise.all([
      fetchAPI(`/api/chat/${id}`).catch(() => null),
      fetchAPI(`/api/chat`).catch(() => null),
    ])
      .then(([roomData, roomsData]) => {
        const rd = roomData as Record<string, unknown> | null;
        setMessages(((rd?.messages ?? []) as ChatMessageItem[]) ?? []);

        const list = roomsData as Record<string, unknown> | null;
        const roomList = ((list?.rooms ?? list?.items ?? []) as RoomInfo[]) ?? [];
        setRoom(roomList.find((r) => String(r.id) === String(roomId)) ?? { id: roomId });
      })
      .finally(() => setLoading(false));
  }, [user, roomId]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async () => {
    const text = draft.trim();
    if (!text || !user || !roomId) return;
    setSending(true);
    try {
      const id = Number(roomId);
      const res = await fetchAPI<Record<string, unknown>>(`/api/chat/${id}/messages`, {
        method: "POST",
        body: JSON.stringify({ content: text }),
      });
      const msg = res?.message as ChatMessageItem | undefined;
      if (msg) setMessages((prev) => [...prev, msg]);
      setDraft("");
    } catch {
      // graceful: ignore send failures
    } finally {
      setSending(false);
    }
  };

  if (authLoading || !user) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  const roomTitle = room?.name ?? room?.title ?? `Room #${roomId}`;

  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <Link href="/chat" className="text-muted-foreground hover:text-foreground transition-colors">
          <ArrowLeft className="h-5 w-5" />
        </Link>
        <div>
          <h1 className="text-2xl font-bold tracking-tight">{roomTitle}</h1>
          <p className="text-xs text-muted-foreground">Chat room</p>
        </div>
      </div>

      <Card className="border-border/50">
        <CardContent className="p-0">
          {loading ? (
            <div className="flex justify-center py-16">
              <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
            </div>
          ) : (
            <div className="flex flex-col h-[60vh]">
              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-3">
                {messages.length === 0 ? (
                  <div className="h-full flex flex-col items-center justify-center text-muted-foreground">
                    <MessageSquare className="h-10 w-10 mb-3 opacity-30" />
                    <p className="text-sm">No messages yet. Say hello!</p>
                  </div>
                ) : (
                  messages.map((m) => {
                    const mine = m.sender_id != null && user && Number(m.sender_id) === user.id;
                    return (
                      <div key={String(m.id)} className={`flex ${mine ? "justify-end" : "justify-start"}`}>
                        <div
                          className={`max-w-[75%] rounded-2xl px-4 py-2 ${
                            mine ? "bg-primary text-primary-foreground" : "bg-muted text-foreground"
                          }`}
                        >
                          {!mine && m.sender_name && m.sender_name !== "System" && (
                            <p className="text-xs font-medium text-primary mb-0.5">{m.sender_name}</p>
                          )}
                          <p className="text-sm whitespace-pre-wrap break-words">{m.content}</p>
                          {m.created_at && (
                            <p
                              className={`text-[10px] mt-1 ${
                                mine ? "text-primary-foreground/70" : "text-muted-foreground"
                              }`}
                            >
                              {new Date(m.created_at).toLocaleTimeString([], {
                                hour: "2-digit",
                                minute: "2-digit",
                              })}
                            </p>
                          )}
                        </div>
                      </div>
                    );
                  })
                )}
                <div ref={endRef} />
              </div>

              {/* Composer */}
              <div className="border-t border-border p-3 flex items-center gap-2">
                <Input
                  value={draft}
                  onChange={(e) => setDraft(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault();
                      send();
                    }
                  }}
                  placeholder="Type a message..."
                  className="rounded-xl"
                />
                <Button
                  onClick={send}
                  disabled={sending || !draft.trim()}
                  size="icon"
                  className="rounded-xl shrink-0"
                >
                  {sending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
