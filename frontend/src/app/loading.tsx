import { HeroSkeleton, ListSkeleton } from "@/components/skeletons";

export default function HomeLoading() {
  return (
    <div>
      <HeroSkeleton />
      <div className="container mx-auto px-4 py-12">
        <div className="mb-6">
          <div className="h-8 w-48 bg-muted rounded animate-pulse mb-2" />
        </div>
        <ListSkeleton count={6} />
      </div>
    </div>
  );
}
