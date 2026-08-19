import { ListSkeleton } from "@/components/skeletons";

export default function AttractionsLoading() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="h-8 w-48 bg-muted rounded animate-pulse mb-2" />
      <div className="h-4 w-64 bg-muted rounded animate-pulse mb-8" />
      <ListSkeleton count={6} />
    </div>
  );
}
