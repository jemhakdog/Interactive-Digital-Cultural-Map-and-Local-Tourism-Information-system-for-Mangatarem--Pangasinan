export interface Attraction {
  id: number;
  name?: string;
  category?: string;
  description?: string;
  directions?: string;
  image_url?: string;
  latitude?: number | null;
  longitude?: number | null;
  status?: string;
}

export interface EventItem {
  id: number;
  name?: string;
  category?: string;
  description?: string;
  date?: string;
  location?: string;
  image_url?: string;
  latitude?: number | null;
  longitude?: number | null;
  status?: string;
}

export interface GalleryItem {
  id: number;
  caption?: string;
  url?: string;
  type?: string;
  status?: string;
}

export interface Announcement {
  id: number;
  title?: string;
  content?: string;
  status?: string;
  created_at?: string;
}

export interface Reply {
  id: number;
  comment?: string;
  created_at?: string;
  user?: { username?: string; role?: string };
}

export interface Review {
  id: number;
  rating?: number | null;
  comment?: string;
  created_at?: string;
  user?: { username?: string; role?: string };
  attraction?: { name?: string };
  replies?: Reply[];
}
