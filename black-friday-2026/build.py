from pathlib import Path
import re, html

root=Path(__file__).parent
copy=(root/'copy-original.txt').read_text(encoding='utf-8-sig')
def esc(s): return html.escape(s.strip())
def section(n):
    m=re.search(r'\[BLOCO '+str(n)+r' — [^\]]+\]\s*(.*?)(?=\[BLOCO |$)',copy,re.S)
    return re.sub(r'\n_+\s*','\n',m.group(1)).strip()
def paras(s):
    result=[p.strip() for p in re.split(r'\n\s*\n',s) if p.strip()]
    if result and '\n' in result[0]: result=result[0].split('\n',1)+result[1:]
    return result
def p(s,cls=''): return '<p class="'+cls+'">'+esc(s).replace('\n','<br>')+'</p>'
def cta(text='Quero abrir meu CNPJ com 30% OFF',secondary=False):
    return '<button type="button" class="cta '+('outline' if secondary else '')+'" data-preview>'+esc(text)+'<span aria-hidden="true">↗</span></button>'
def label(n,title): return '<p class="eyebrow"><span>'+str(n).zfill(2)+'</span> '+title+'</p>'
def wrap(n,title,body,cls=''):
    if n in (6,9): body='<div class="section-body">'+body+'</div><div class="section-action">'+cta()+'</div>'
    return '<section class="section '+cls+'" id="bloco-'+str(n)+'"><div class="wrap">'+label(n,title)+body+'</div></section>'
def heading(s): return '<h2>'+esc(s)+'</h2>'

blocks=[]
a=paras(section(1)); blocks.append(wrap(1,'O QUE MUDA EM 2027','<div class="editorial"><div>'+heading(a[0])+'</div><div>'+''.join(p(x) for x in a[1:])+'</div></div>','tonal'))

rows=[('O que é','Inscrição para fins cadastrais e fiscais','Pessoa jurídica de verdade'),('Você continua sendo','Pessoa física','Sócio da sua própria sociedade'),('Imposto de Renda','Tabela da pessoa física, até 27,5%','Pode optar pelo Simples Nacional'),('Simples Nacional','Não se aplica','Anexo IV, a partir de 4,5%'),('Nota fiscal de serviço','Conforme as novas regras','Emissão pela plataforma Advventure')]
table='<div class="table-scroll"><table><thead><tr><th>Entenda a diferença</th><th>CNPJ técnico</th><th>Sociedade Unipessoal<br>de Advocacia</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<'+('th scope="row"' if i==0 else 'td')+'>'+esc(x)+'</'+('th' if i==0 else 'td')+'>' for i,x in enumerate(row))+'</tr>' for row in rows)+'</tbody></table></div>'
a=paras(section(2)); blocks.append(wrap(2,'CNPJ TÉCNICO NÃO É EMPRESA',heading(a[0])+table+''.join(p(x,'note' if 'nanoempreendedor' in x else '') for x in a[1:] if not x.startswith('CNPJ técnico'))))

a=paras(section(3)); note=next(x for x in a if x.startswith('*Exemplo'))
blocks.append(wrap(3,'A CONTA QUE NINGUÉM FAZ COM VOCÊ',heading(a[0])+'''<div class="simulation"><div class="cpf"><span class="eyebrow">RECEBENDO NO CPF</span><p>Honorários mensais: R$ 20.000</p><strong>≈ R$ 4.591</strong><span>IRPF por mês · até 27,5%</span></div><div class="cnpj"><span class="eyebrow">SOCIEDADE NO SIMPLES</span><p>Honorários mensais: R$ 20.000</p><strong>≈ R$ 1.125<span>*</span></strong><span>DAS por mês · Anexo IV · ≈ 5,625% efetiva</span></div></div><div class="difference"><span>DIFERENÇA ILUSTRATIVA</span><strong>≈ R$ 3.466<span>/mês</span></strong><p>Mais de R$ 40 mil por ano.</p></div>'''+p('E quanto mais você fatura, maior a diferença fica.')+p(note,'note')+cta('Quero fazer a minha conta e abrir meu CNPJ'),'tonal'))

a=section(4); opening,migration=a.split('Já tem CNPJ',1)
def pathcontent(s): return ''.join(p(x) for x in paras(s) if not x.startswith('Botão:'))
blocks.append(wrap(4,'QUAL DOS DOIS É VOCÊ?','<div class="paths"><article><span class="path-no">01 / ABERTURA</span>'+heading('Ainda recebe no CPF')+pathcontent(opening.replace('Ainda recebe no CPF','',1))+cta()+'</article><article><span class="path-no">02 / MIGRAÇÃO</span>'+heading('Já tem CNPJ')+pathcontent(migration)+cta('Quero migrar com o 1º mês grátis',True)+'</article></div>'))

a=paras(section(5)); features=next(x for x in a if x.startswith('* ')); intro=[x for x in a[1:] if x!=features and not x.startswith('Automação')]
blocks.append(wrap(5,'POR QUE A ADVVENTURE','<div class="editorial"><div>'+heading(a[0])+''.join(p(x) for x in intro)+'</div><div><ul class="features">'+''.join('<li>'+esc(x.lstrip('* '))+'</li>' for x in features.split('\n') if x.strip())+'</ul></div></div><p class="statement">Automação no que é burocrático.<br><em>Atendimento humano no que realmente importa.</em></p>','tonal'))

a=section(6); left,right=a.split('Migração de contabilidade',1)
def process(s):
    items=re.findall(r'^\d+\. (.+)$',s,re.M)
    return '<ol class="steps">'+''.join('<li>'+esc(x)+'</li>' for x in items)+'</ol>'
note=next(x for x in paras(left) if x.startswith('As taxas'))
blocks.append(wrap(6,'COMO FUNCIONA',heading('Da decisão ao próximo capítulo.')+'<div class="process-grid"><div><h3>Abertura de CNPJ</h3>'+process(left)+'</div><div><h3>Migração de contabilidade</h3>'+process(right)+'</div></div>'+p(note,'note')))

a=paras(section(7)); authority=''.join(p(x) for x in a[1:] if not x.startswith('Visual:'))
blocks.append(wrap(7,'QUEM ESTÁ POR TRÁS','<div class="authority"><div class="authority-photo"><img src="assets/gabriel-sorrindo.jpeg" width="1066" height="1600" loading="lazy" alt="Gabriel Quintanilha sorrindo, com terno azul e gravata vermelha"><span>GABRIEL QUINTANILHA<br><small>Tributarista · Idealizador da Advventure</small></span></div><div>'+heading(a[0])+authority+'</div></div>','tonal'))

a=paras(section(8)); blocks.append(wrap(8,'CASOS QUE A GENTE CONHECE BEM',heading('Situações reais.<br>Decisões que fazem diferença.'.replace('<br>',' '))+'<div class="cases">'+''.join('<article><span class="case-index">'+str(i+1).zfill(2)+'</span>'+p(x)+'</article>' for i,x in enumerate(a) if not x.startswith('Nomes fictícios'))+'</div>'+p('Nomes fictícios. As situações e os erros são reais.','note')))

rows=[('Especializado em advocacia','Variável','Não','Só atende advogado'),('Mensalidade','De meio a um salário mínimo','Varia','R$ 189 (R$ 159 com convênio OAB)'),('Visibilidade','Depende do contador','Limitada','Tudo na sua tela'),('Atendimento','Humano, mas opaco','Automatizado','Plataforma com revisão humana')]
table='<div class="table-scroll"><table><thead><tr><th>O que importa</th><th>Contador tradicional</th><th>Plataformas genéricas</th><th>Advventure</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<'+('th scope="row"' if i==0 else 'td')+'>'+esc(x)+'</'+('th' if i==0 else 'td')+'>' for i,x in enumerate(row))+'</tr>' for row in rows)+'</tbody></table></div>'
blocks.append(wrap(9,'COMPARE',heading('Sua advocacia merece especialização.')+table,'tonal'))

blocks.append(wrap(10,'SUPER BLACK FRIDAY ADVVENTURE',heading('A condição para começar<br>2027 do jeito certo.'.replace('<br>',' '))+'''<div class="offers" id="ofertas"><article class="offer primary"><span class="offer-tag">ABERTURA DE CNPJ · 30% OFF</span><p class="old-price">De <s>R$ 600</s> por</p><div class="offer-price">R$ <strong>420</strong></div><p class="installments">6x de R$ 70 sem juros no cartão de crédito</p><ul class="features"><li>Abertura completa, do zero à formalização</li><li>Registro na OAB, CNPJ, Prefeitura e enquadramento no Simples</li><li>1º mês de contabilidade grátis ao contratar a mensalidade junto</li><li>Taxas oficiais à parte, pagas direto aos órgãos</li></ul>'''+cta('Garantir meus 30% OFF')+'''</article><article class="offer"><span class="offer-tag">MIGRAÇÃO · 1º MÊS GRÁTIS</span><p class="old-price">Plano Padrão</p><div class="offer-price small">R$ <strong>189</strong><span>/mês</span></div><p class="installments">R$ 159 com convênio OAB/RJ, MG, SC e PE.<br>Cobrança começando só no 2º mês.</p><ul class="features"><li>Relatórios contábeis e de faturamento</li><li>Envio de DCTF, DEFIS e PGDASD</li><li>Cálculo automático de tributos e emissão de guias</li><li>NFS-e ilimitada e importação de extrato bancário</li><li>Pró-labore para até 2 sócios</li><li>Folha de pagamento sob consulta</li></ul>'''+cta('Migrar e falar com um consultor',True)+'</article></div>'+p('Condição especial de Black Friday por tempo limitado.','offer-note')))

a=paras(section(11)); blocks.append(wrap(11,'GARANTIA',heading(a[0])+'<div class="guarantees">'+''.join('<div>'+p(re.sub(r'\[Revisar.*?\]','',x))+'</div>' for x in a[1:])+'</div>','tonal'))
a=paras(section(12)); entries=[]
for x in a:
    m=re.match(r'"(.*?)"\s*(.*)',x,re.S)
    if m: entries.append('<details><summary>'+esc(m.group(1))+'</summary>'+p(m.group(2))+'</details>')
blocks.append(wrap(12,'ANTES DO PRÓXIMO PASSO','<div class="faq-grid"><div>'+heading('Vamos falar sobre suas dúvidas?')+'</div><div class="accordion">'+''.join(entries)+'</div></div>'))

a=paras(section(13)); entries=[]
for x in a:
    q,answer=x.split('?',1); entries.append('<details><summary>'+esc(q)+'?</summary>'+p(answer)+'</details>')
blocks.append(wrap(13,'PERGUNTAS FREQUENTES','<div class="faq-grid"><div>'+heading('Clareza para decidir.')+'<p>Sobre a abertura, a migração e sua rotina com a Advventure.</p></div><div class="accordion">'+''.join(entries)+'</div></div>','tonal'))
a=paras(section(14));blocks.append(wrap(14,'2027 COMEÇA ANTES DE JANEIRO','<div class="closing">'+heading(a[0])+p(a[1])+ '<div class="closing-actions">'+cta()+cta('Já tenho CNPJ e quero migrar',True)+'</div></div>'))

hero='''<a class="skip" href="#conteudo">Pular para o conteúdo</a><header class="topbar"><div class="marquee" aria-label="Super Black Friday Advventure, 30% OFF na abertura de CNPJ, 6x sem juros"><div aria-hidden="true">'''+('SUPER BLACK FRIDAY ADVVENTURE <b>●</b> 30% OFF NA ABERTURA DE CNPJ <b>●</b> 6X SEM JUROS <b>●</b> CONDIÇÃO POR TEMPO DETERMINADO <b>●</b> 2027 COMEÇA ANTES DE JANEIRO <b>●</b> ')*2+'''</div></div></header><main id="conteudo"><section class="hero"><div class="wrap hero-inner"><div class="hero-copy"><img class="campaign-logo" src="assets/logo-campanha.png" width="2172" height="724" alt="Black Friday 2026 Advventure Contabilidade"><p class="eyebrow hero-eyebrow">SUPER BLACK FRIDAY ADVVENTURE <span class="mobile-hide">· 2027 COMEÇA ANTES DE JANEIRO</span></p><h1>Advogado, entre em 2027 com o <em>regime tributário certo.</em></h1><p class="hero-sub">Abrir CNPJ é burocrático, mas não precisa ser caro. Na Super Black Friday antecipada, a Advventure abre o seu com 30% de desconto, de R$ 600 por R$ 420, em 6x de R$ 70 sem juros. Se você já tem CNPJ, migre com o 1º mês de contabilidade grátis.</p><div class="hero-price"><span>De <s>R$ 600</s> por</span><strong>R$ 420</strong><span>6x de R$ 70<br>sem juros</span></div><div class="hero-actions">'''+cta()+cta('Já tenho CNPJ e quero migrar',True)+'''</div><p class="hero-proof">Contabilidade feita de advogados para advogados · Idealizada pelo tributarista Gabriel Quintanilha · Convênio com 4 seccionais da OAB</p></div><div class="hero-art"><div class="halo"></div><img src="assets/gabriel-recortado.png" alt="Gabriel Quintanilha, idealizador da Advventure, de terno azul com as mãos entrelaçadas" width="1024" height="1536" fetchpriority="high"><div class="discount"><strong>30%</strong><span>OFF NA ABERTURA</span></div><div class="expert-label"><strong>Gabriel Quintanilha</strong><span>Tributarista · Idealizador da Advventure</span></div></div><div class="timeline" aria-label="Linha do tempo da virada do ano"><span data-month="10">OUT</span><i></i><span data-month="11">NOV</span><i></i><span data-month="12">DEZ</span><i></i><strong>JAN/2027</strong></div></div></section>'''
footer='''</main><footer><div class="wrap footer-inner"><img src="assets/logo-campanha.png" width="2172" height="724" alt="Advventure Black Friday 2026" loading="lazy"><p>Advventure Contabilidade<br><span>Contabilidade feita de advogados para advogados</span></p><div><button data-legal="Termos de Uso">Termos de Uso</button><button data-legal="Política de Privacidade">Política de Privacidade</button></div></div></footer><aside class="review-mode" aria-label="Página em aprovação">PRÉVIA PARA APROVAÇÃO <span>·</span> Contratação ainda indisponível</aside><dialog id="preview-dialog" aria-labelledby="dialog-title"><button class="dialog-close" aria-label="Fechar">×</button><p class="eyebrow">SUPER BLACK FRIDAY ADVVENTURE</p><h2 id="dialog-title">Em breve.</h2><p id="dialog-message">Esta página está em aprovação. O link de contratação será disponibilizado após a validação da campanha.</p><button class="cta dialog-dismiss">Entendi</button></dialog><script src="app.js" defer></script>'''
doc='<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#02040b"><meta name="description" content="Super Black Friday Advventure 2026. Abertura de CNPJ com 30% OFF ou migração com o primeiro mês de contabilidade grátis."><title>Super Black Friday 2026 | Advventure Contabilidade</title><link rel="stylesheet" href="style.css"></head><body>'+hero+''.join(blocks)+footer+'</body></html>'
(root/'index.html').write_text(doc,encoding='utf-8')
print('Built index.html: 14 content sections + hero; '+str(len(doc))+' characters')
