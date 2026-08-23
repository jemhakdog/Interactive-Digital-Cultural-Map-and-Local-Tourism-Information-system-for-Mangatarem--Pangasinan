"use client";

import { useEffect, useState, useCallback } from "react";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { fetchAPI } from "@/lib/api";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Loader2, CalendarCheck } from "lucide-react";

interface Booking {
  id: number;
  date: string;
  asset: string;
  tourist: string;
  party_size: number;
  status: string;
}

const STATUS_CLASS: Record<string, string> = {
  confirmed: "bg-green-50 text-green-700 border-green-200",
  pending: "bg-yellow-50 text-yellow-700 border-yellow-200",
  cancelled: "bg-red-50 text-red-700 border-red-200",
  attended: "bg-blue-50 text-blue-700 border-blue-200",
  "no-show": "bg-gray-50 text-gray-600 border-gray-200",
};

export default function AdminBookingsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  // GET /api/booking/admin/list returns all reservations (admin|contributor|business_owner).
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [info, setInfo] = useState<string | null>(null);

  const load = useCallback(() => {
    return fetchAPI<Booking[]>("/api/booking/admin/list")
      .then((data) => setBookings(data ?? []))
      .catch(() => setBookings([]));
  }, []);

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/dashboard");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    load().finally(() => setLoading(false));
  }, [user, load]);

  const handleStatusChange = async (id: number, status: string) => {
    // POST /api/booking/admin/update-status exists for admin|contributor|business_owner.
    try {
      await fetchAPI("/api/booking/admin/update-status", {
        method: "POST",
        body: JSON.stringify({ reservation_id: id, status }),
      });
      setBookings((prev) => prev.map((b) => (b.id === id ? { ...b, status } : b)));
      setInfo("Reservation status updated.");
    } catch {
      setInfo("Could not update status — the reservation may already be in that state or the transition is not allowed.");
    }
  };

  if (authLoading || !user || loading) {
    return (
      <div className="flex justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <CalendarCheck className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Booking Management</h1>
          <p className="text-muted-foreground text-sm mt-0.5">
            Review and update reservation statuses
          </p>
        </div>
      </div>

      {info && (
        <div className="mb-4 rounded-lg border border-border bg-muted px-4 py-3 text-sm text-muted-foreground">
          {info}
        </div>
      )}

      <div className="border rounded-xl border-border/50 overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead>Date</TableHead>
              <TableHead>Asset</TableHead>
              <TableHead>Tourist</TableHead>
              <TableHead>Party</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {bookings.map((b) => (
              <TableRow key={b.id}>
                <TableCell className="text-sm">{b.date}</TableCell>
                <TableCell className="font-medium">{b.asset}</TableCell>
                <TableCell className="text-sm">{b.tourist}</TableCell>
                <TableCell className="text-sm">{b.party_size}</TableCell>
                <TableCell>
                  <Badge
                    variant="outline"
                    className={`text-xs capitalize ${STATUS_CLASS[b.status] ?? ""}`}
                  >
                    {b.status}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <select
                    value={b.status}
                    onChange={(e) => handleStatusChange(b.id, e.target.value)}
                    className="rounded-lg border border-border bg-background px-2 py-1.5 text-sm text-foreground outline-none focus:ring-2 focus:ring-primary/40"
                  >
                    <option value="pending">Pending</option>
                    <option value="confirmed">Confirmed</option>
                    <option value="attended">Attended</option>
                    <option value="no-show">No-show</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                </TableCell>
              </TableRow>
            ))}
            {bookings.length === 0 && (
              <TableRow>
                <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                  No reservations found.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
