# PROMOB MVP - Configurador ColorGlass

MVP inicial de configurador 3D tecnico para orcar cristaleiras com MDF, portas de aluminio e vidro.

Stack: React, Vite, TypeScript, Three.js, React Three Fiber, Drei, Zustand e Zod.

Rodar local:

cd PROMOB
npm install
npm run dev

Build:

cd PROMOB
npm install
npm run build

Deploy no Render pelo painel:

Root Directory: PROMOB
Build Command: npm install && npm run build
Publish Directory: dist

O MVP configura altura, largura, profundidade, espessuras de MDF, portas, perfil, vidro, margem e perda. Ele calcula vao util, portas, area de MDF, area de vidro, metros de perfil, baguete, kits de montagem, custo e venda sugerida. Tambem mostra visualizacao 3D tecnica.

Proximas etapas: PDF de orcamento, plano de corte, Supabase, cadastro de clientes e regras industriais por perfil.
