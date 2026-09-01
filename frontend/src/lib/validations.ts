import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().email("Enter a valid email"),
  password: z.string().min(1, "Password is required"),
  remember: z.boolean().optional(),
});
export type LoginInput = z.infer<typeof loginSchema>;

export const registerSchema = z
  .object({
    name: z.string().min(2, "Name must be at least 2 characters"),
    email: z.string().email("Enter a valid email"),
    password: z.string().min(6, "Password must be at least 6 characters"),
    confirm: z.string().min(1, "Confirm your password"),
    role: z.enum(["user", "contributor", "business_owner"]),
    barangay: z.string().optional(),
  })
  .refine((d) => d.password === d.confirm, {
    message: "Passwords do not match",
    path: ["confirm"],
  });
export type RegisterInput = z.infer<typeof registerSchema>;

export const reviewSchema = z.object({
  rating: z.number().int().min(1, "Select a rating").max(5),
  comment: z.string().min(1, "Comment is required").max(1000),
});
export type ReviewInput = z.infer<typeof reviewSchema>;

export const attractionSchema = z.object({
  name: z.string().min(2, "Name is required"),
  description: z.string().min(1, "Description is required"),
  category: z.string().min(1, "Category is required"),
  latitude: z.union([z.number(), z.string()]).optional(),
  longitude: z.union([z.number(), z.string()]).optional(),
});
export type AttractionInput = z.infer<typeof attractionSchema>;

export const eventSchema = z.object({
  name: z.string().min(2, "Name is required"),
  description: z.string().min(1, "Description is required"),
  category: z.string().optional(),
  date: z.string().min(1, "Date is required"),
  location: z.string().min(1, "Location is required"),
});
export type EventInput = z.infer<typeof eventSchema>;
