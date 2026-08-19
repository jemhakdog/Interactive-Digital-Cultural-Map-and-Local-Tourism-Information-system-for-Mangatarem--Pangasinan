export interface AttractionItem {
  id: number;
  name: string;
  description?: string | null;
  category?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  image_url?: string | null;
  barangay_id?: number | null;
  barangay_name?: string | null;
  status?: string;
  is_featured?: boolean;
  physical_status?: string | null;
  is_verified?: boolean;
  opening_hours?: string | null;
  entrance_fee?: string | null;
  contact_info?: string | null;
  facilities?: string[] | string | null;
  advisory_message?: string | null;
  advisory_status?: string | null;
  directions?: string | null;
  osm_alternatives?: string | null;
  heritage_profile_id?: number | null;
  heritage_asset_type?: string | null;
  rating?: number | null;
  review_count?: number | null;
  created_at?: string | null;
  distance?: number | null;
  // Curated enhancements
  gallery?: string[];
  highlights?: string[];
  activities?: string[];
  best_time_to_visit?: string;
  what_to_bring?: string[];
  elevation?: string;
  difficulty?: "Easy" | "Moderate" | "Challenging" | "Scenic Drive";
}

export interface AttractionReviewItem {
  id: number;
  user_id: number;
  username: string;
  attraction_id: number;
  establishment_id?: number | null;
  rating: number;
  comment: string;
  status: string;
  parent_id?: number | null;
  created_at: string | null;
  photos?: { id: number; url: string }[];
  replies?: AttractionReviewItem[];
}

export interface AttractionReviewSummary {
  average: number;
  total: number;
  distribution: {
    "1": number;
    "2": number;
    "3": number;
    "4": number;
    "5": number;
  };
}
