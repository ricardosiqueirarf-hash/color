import { costs, glasses, profiles } from '../data/catalog';
import type { CristaleiraCalculation, CristaleiraConfig, MaterialLine } from '../types/configuratorTypes';

const m = (mm: number) => mm / 1000;
const r = (value: number) => Math.round(value * 100) / 100;

export function calculateCristaleira(config: CristaleiraConfig): CristaleiraCalculation {
  const profile = profiles[config.profileId as keyof typeof profiles];
  const glass = glasses[config.glassId as keyof typeof glasses];
  const waste = 1 + config.wastePercent / 100;

  const usefulWidthMm = Math.max(config.widthMm - config.sideMdfMm * 2, 0);
  const usefulHeightMm = Math.max(config.heightMm - config.topMdfMm - config.bottomMdfMm, 0);
  const usefulDepthMm = Math.max(config.depthMm - (config.hasBackPanel ? config.backMdfMm : 0), 0);

  const overlapMm = config.openingType === 'correr' ? 30 : 0;
  const doorWidthMm = config.openingType === 'correr'
    ? (usefulWidthMm + overlapMm * Math.max(config.doorCount - 1, 0)) / config.doorCount
    : usefulWidthMm / config.doorCount;
  const doorHeightMm = usefulHeightMm;

  const doorAreaM2 = m(doorWidthMm) * m(doorHeightMm);
  const doorPerimeterM = 2 * m(doorWidthMm) + 2 * m(doorHeightMm);
  const totalGlassAreaM2 = doorAreaM2 * config.doorCount * waste;
  const totalProfileMl = doorPerimeterM * config.doorCount * waste;
  const totalBaguetteMl = totalProfileMl;

  const mdfAreaM2 = (
    m(config.heightMm) * m(config.depthMm) * 2 +
    m(config.widthMm) * m(config.depthMm) * 2 +
    (config.hasBackPanel ? m(config.widthMm) * m(config.heightMm) : 0) +
    m(usefulWidthMm) * m(usefulDepthMm) * config.shelfCount
  ) * waste;

  const materialLines: MaterialLine[] = [
    { name: 'MDF total aproximado', quantity: `${r(mdfAreaM2)} m²`, cost: mdfAreaM2 * costs.mdfPricePerM2 },
    { name: profile.name, quantity: `${r(totalProfileMl)} m`, cost: totalProfileMl * profile.pricePerMeter },
    { name: glass.name, quantity: `${r(totalGlassAreaM2)} m²`, cost: totalGlassAreaM2 * glass.pricePerM2 },
    { name: 'Baguete PVC', quantity: `${r(totalBaguetteMl)} m`, cost: totalBaguetteMl * costs.baguettePricePerMeter },
    { name: 'Kit montagem', quantity: `${config.doorCount} kit(s)`, cost: config.doorCount * costs.assemblyKitPerDoor },
    { name: 'Mão de obra estimada', quantity: '1 módulo', cost: costs.laborPerModule + config.doorCount * costs.laborPerDoor },
  ];

  const subtotalCost = materialLines.reduce((sum, item) => sum + item.cost, 0);
  const salePrice = subtotalCost / (1 - config.marginPercent / 100);

  return {
    useful: { usefulWidthMm, usefulHeightMm, usefulDepthMm },
    door: { widthMm: doorWidthMm, heightMm: doorHeightMm, glassAreaM2: doorAreaM2, profileMl: doorPerimeterM, baguetteMl: doorPerimeterM, kitCount: 1 },
    totalGlassAreaM2,
    totalProfileMl,
    totalBaguetteMl,
    mdfAreaM2,
    kitCount: config.doorCount,
    materialLines,
    subtotalCost,
    salePrice,
    pricePerDoor: salePrice / config.doorCount,
  };
}
