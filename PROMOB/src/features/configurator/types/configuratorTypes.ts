export type DoorOpeningType = 'giro' | 'correr';
export type AluminumColor = 'preto' | 'bronze' | 'prata' | 'dourado' | 'inox';

export interface CristaleiraConfig {
  product: 'cristaleira';
  heightMm: number;
  widthMm: number;
  depthMm: number;
  sideMdfMm: number;
  topMdfMm: number;
  bottomMdfMm: number;
  backMdfMm: number;
  hasBackPanel: boolean;
  shelfThicknessMm: number;
  shelfCount: number;
  doorCount: number;
  openingType: DoorOpeningType;
  profileId: string;
  aluminumColor: AluminumColor;
  glassId: string;
  glassThicknessMm: number;
  wastePercent: number;
  marginPercent: number;
}

export interface UsefulMeasures {
  usefulWidthMm: number;
  usefulHeightMm: number;
  usefulDepthMm: number;
}

export interface DoorCalculation {
  widthMm: number;
  heightMm: number;
  glassAreaM2: number;
  profileMl: number;
  baguetteMl: number;
  kitCount: number;
}

export interface MaterialLine {
  name: string;
  quantity: string;
  cost: number;
}

export interface CristaleiraCalculation {
  useful: UsefulMeasures;
  door: DoorCalculation;
  totalGlassAreaM2: number;
  totalProfileMl: number;
  totalBaguetteMl: number;
  mdfAreaM2: number;
  kitCount: number;
  materialLines: MaterialLine[];
  subtotalCost: number;
  salePrice: number;
  pricePerDoor: number;
}
