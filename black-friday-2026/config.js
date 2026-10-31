'use strict';
// CONFIGURAÇÃO DA CAMPANHA. Edite somente os valores entre aspas/números.
// Não reutilize checkout de outra oferta: insira o link específico desta Black Friday.
window.ADVVENTURE_CONFIG = {
  // ABERTURA DE CNPJ (30% OFF): o botão abre uma janela com as duas formas de pagamento
  cardUrl: 'https://www.asaas.com/000/c/oxu862lv9kn33enq',      // Asaas · cartão em até 6x
  pixUrl: 'https://www.asaas.com/000/c/w5ba4t5j7a5z2t1s',       // Asaas · Pix ou boleto (R$ 420)

  // MIGRAÇÃO / CONTABILIDADE MENSAL: o botão abre uma janela com os dois planos
  monthlyUrl: 'https://www.asaas.com/000/c/zfkp2qrcm0dir97m',   // Asaas · Plano Padrão R$ 189
  monthlyOabUrl: 'https://www.asaas.com/000/c/gdi3jrju8s7ts9kc', // Asaas · convênio OAB R$ 159

  // WhatsApp do comercial (bloco "Ainda está com dúvida?" abaixo das ofertas)
  consultantUrl: 'https://wa.me/5511995148774?text=Ol%C3%A1!%20Vi%20a%20Black%20Friday%20da%20Advventure%20e%20tenho%20uma%20d%C3%BAvida%20antes%20de%20contratar.',

  termsUrl: '',                 // Sem página de Termos no site da Advventure: o botão fica oculto enquanto vazio.
  privacyUrl: '',               // Sem Política de Privacidade no site: o botão fica oculto enquanto vazio.
  reviewMode: false,            // Página aprovada pelo cliente em 31/10/2026.
  originalPrice: 600,
  openingPrice: 420,
  installments: 6,
  illustrativeInstallment: 72.61, // Parcela no cartão com as taxas (informada pela Advventure).
  cardTotal: 435.66
};
