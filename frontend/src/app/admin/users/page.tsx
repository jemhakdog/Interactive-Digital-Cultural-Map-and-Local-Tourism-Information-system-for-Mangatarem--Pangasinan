"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Loader2, Users } from "lucide-react";

interface UserRow {
  id: number;
  name: string;
  email: string;
  role: string;
  is_approved: boolean;
}

export default function AdminUsersPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [users, setUsers] = useState<UserRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || user.role !== "admin") return;
    let cancelled = false;
    const loadUsers = async () => {
      try {
        const data = await fetchAPI<{ users: UserRow[]; total: number }>(
          "/api/admin/users?page=1&per_page=100"
        );
        if (!cancelled) setUsers(data.users);
      } catch {
        if (!cancelled) setError("Failed to load users.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    loadUsers();
    return () => {
      cancelled = true;
    };
  }, [user]);

  if (authLoading || !user || loading) {
    return <div className="flex justify-center py-16"><Loader2 className="h-6 w-6 animate-spin text-muted-foreground" /></div>;
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <Users className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Manage Users</h1>
          <p className="text-muted-foreground text-sm mt-0.5">User management</p>
        </div>
      </div>

      <div className="border rounded-xl border-border/50 overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {error ? (
              <TableRow>
                <TableCell colSpan={4} className="text-center text-destructive py-8">
                  {error}
                </TableCell>
              </TableRow>
            ) : users.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className="text-center text-muted-foreground py-8">
                  No users found.
                </TableCell>
              </TableRow>
            ) : (
              users.map((u) => (
                <TableRow key={u.id}>
                  <TableCell className="font-medium">{u.name}</TableCell>
                  <TableCell>{u.email}</TableCell>
                  <TableCell className="capitalize">{u.role}</TableCell>
                  <TableCell>
                    <Badge variant={u.is_approved ? "default" : "secondary"}>
                      {u.is_approved ? "Approved" : "Pending"}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
