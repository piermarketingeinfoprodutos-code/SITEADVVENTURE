# Super Black Friday 2026 — Advventure

Página estática de aprovação da Pier. HTML, CSS e JavaScript, sem dependências de instalação. Para publicar, copie `index.html`, `style.css`, `app.js` e `assets/` para o diretório desejado. Todos os caminhos são relativos; funciona também em `/black-friday-2026/`.

## Conteúdo e revisão

Fonte: Google Doc `1juEWBij8_s606Ca8Y1LgNI-VY1STkvgB-rPuEhP6pSI`, versão V2. Cópia de referência em `copy-original.txt`. `build.py` gera o HTML a partir dessa copy e das estruturas de comparação/oferta.

- Os CTAs abrem aviso de aprovação. Não há checkout, WhatsApp, coleta de dados, analytics ou pagamentos.
- Antes do lançamento, substituir os eventos `data-preview` pelos destinos definitivos de cada trilha e vincular Termos de Uso e Política de Privacidade.
- Validar tabela de reembolso parcial para honorário de R$ 420, conforme pendência expressa na copy. A observação editorial não aparece como texto comercial.
- Revisar as condições comerciais, as afirmações tributárias para 2027, a comparação ilustrativa e as credenciais antes da campanha definitiva. Conteúdo mantido conforme documento fornecido.
- O documento solicita foto sentada à mesa e fotos do escritório; esses arquivos não foram fornecidos. A seção de autoridade usa a foto oficial sorrindo já enviada. Não foram inventadas fotos do escritório.
- O hero usa recorte gerado a partir da foto oficial de mãos entrelaçadas. O restante usa fotografia original.
- A linha do tempo inclui OUT para representar o mês atual da montagem e destaca JAN/2027. O mês ativo segue America/Sao_Paulo.
- Sem contagem regressiva, formulários ou links fictícios.

## Prévia local

`python -m http.server 8765 --directory black-friday-2026`

## Regerar HTML

`python black-friday-2026/build.py`
