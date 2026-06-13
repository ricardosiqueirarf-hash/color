import { create } from 'zustand';
import type { CristaleiraConfig } from '../types/configuratorTypes';

const initialConfig: CristaleiraConfig = {
  product: 'cristaleira',
  heightMm: 2200,
  widthMm: 1000,
  depthMm: 450,
  sideMdfMm: 18,
  topMdfMm: 18,
  bottomMdfMm: 18,
  backMdfMm: 6,
  hasBackPanel: true,
  shelfThicknessMm: 18,
  shelfCount: 4,
  doorCount: 2,
  openingType: 'giro',
  profileId: '1036',
  aluminumColor: 'preto',
  glassId: 'reflecta_bronze',
  glassThicknessMm: 4,
  wastePercent: 10,
  marginPercent: 45,
};

interface ConfiguratorStore {
  config: CristaleiraConfig;
  updateConfig: (patch: Partial<CristaleiraConfig>) => void;
  resetConfig: () => void;
}

export const useConfiguratorStore = create<ConfiguratorStore>((set) => ({
  config: initialConfig,
  updateConfig: (patch) => set((state) => ({ config: { ...state.config, ...patch } })),
  resetConfig: () => set({ config: initialConfig }),
}));
