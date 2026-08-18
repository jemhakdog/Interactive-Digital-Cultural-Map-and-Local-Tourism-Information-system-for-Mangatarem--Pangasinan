# Explanation: User Registration and Validation Flowchart

This flowchart outlines the logic used to maintain data integrity and representative accountability during the onboarding process.

### Critical Decisions:
1.  **Identity Verification**: The system first checks for username and email uniqueness to prevent duplicate accounts.
2.  **Role Branching**:
    - **Visitors**: Granted immediate access to the platform upon registration.
    - **Contributors**: Subjected to stricter validation protocols.
3.  **Barangay Representative Constraint**: A pivotal logic gate ensures that each Barangay has only **one** approved representative at a time. If a representative is already registered for the selected barangay, subsequent contributor applications for that area are automatically blocked.
4.  **Approval Workflow**: New contributors are placed in a **Pending Approval** state. They are restricted from editing the map until a system administrator verifies their credentials, ensuring the accuracy of cultural and tourism information.
