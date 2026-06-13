import { z } from 'zod';

export const configuratorSchema = z.object({
  heightMm: z.number().min(300).max(3000),
  widthMm: z.number().min(300).max(3000),
  depthMm: z.number().min(100).max(1000),
  sideMdfMm: z.number().min(6).max(30),
  topMdfMm: z.number().min(6).max(30),
  bottomMdfMm: z.number().min(6).max(30),
  backMdfMm: z.number().min(0).max(30),
  shelfThicknessMm: z.number().min(6).max(30),
  shelfCount: z.number().min(0).max(20),
  doorCount: z.number().min(1).max(6),
  wastePercent: z.number().min(0).max(50),
  marginPercent: z.number().min(0).max(300),
});
