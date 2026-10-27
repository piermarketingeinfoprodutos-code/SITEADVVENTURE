from pathlib import Path
import re,html

def render(doc):
    source=(Path(__file__).parent/'COPY-FINAL.md').read_text(encoding='utf-8').split('\n---\n')[0]
    pieces=re.split(r'^## (\d+)\. ([^\n]+)\n',source,flags=re.M)
    sections=[(int(pieces[i]),pieces[i+1],pieces[i+2]) for i in range(1,len(pieces),3)]
    sim=re.search(r'<div class="calculator">.*?</details>',doc,re.S).group(0)
    sim=re.sub(r'<div class="amount-options">.*?</div>','<div class="amount-options">'+''.join(f'<button type="button" data-amount="{v}"'+(' aria-pressed="true"' if v==10000 else '')+f'>R$ {v//1000} mil</button>' for v in (10000,20000,30000,50000))+'</div>',sim,flags=re.S)
    sim=sim.replace('min="1"','min="10000"').replace('min="1000"','min="10000"').replace('value="20000"','value="10000"').replace('R$ 1 a R$ 50 mil','R$ 10 mil a R$ 50 mil')
    for old,new in [('R$ 4.424,29','R$ 1.674,29'),('R$ 1.125,00','R$ 450,00'),('5,625% efetiva','4,5% efetiva'),('R$ 3.299,29','R$ 1.224,29'),('R$ 39.591,48','R$ 14.691,48')]:sim=sim.replace(old,new)
    sim='<div class="simulation-notice"><strong>SIMULAÇÃO ILUSTRATIVA</strong><span>Referência tributária: 2026. Não é uma promessa de economia.</span></div>'+sim
    comparison='''<div class="tax-comparison"><article class="tax-person"><span class="comparison-tag">RECEBENDO NO CPF</span><h3>Imposto de Renda<br>de até <strong>27,5%</strong></h3><ul><li>O IRPF segue uma tabela progressiva.</li><li>Despesas dedutíveis e livro-caixa podem reduzir a base do imposto.</li><li>Permanecem as obrigações fiscais e previdenciárias da pessoa física.</li><li>Sua estrutura deve ser avaliada individualmente.</li></ul></article><article class="tax-company"><span class="comparison-tag">SOCIEDADE NO SIMPLES NACIONAL</span><h3>Alíquota inicial<br>de <strong>4,5%</strong></h3><ul><li>Advocacia no Anexo IV, conforme a faixa de receita.</li><li>A alíquota efetiva varia com o faturamento acumulado.</li><li>Existem obrigações e custos de manutenção da sociedade.</li><li>Acompanhamento especializado para avaliar o enquadramento e organizar a rotina fiscal.</li></ul></article></div><p class="comparison-note">As alíquotas incidem sobre bases diferentes e não representam, isoladamente, o custo total de cada estrutura. A CPP fica fora do DAS no Anexo IV.</p>'''
    markers={
    '[COMPARACAO]':comparison,
    '[SIMULADOR]':sim,
    '[CALENDARIO]':'<figure class="calendar-visual"><img src="assets/janeiro-2027.png" width="1672" height="941" loading="lazy" alt="Calendário de janeiro de 2027 e Congresso Nacional ao fundo"><figcaption>2027 COMEÇA COM AS DECISÕES QUE VOCÊ TOMA AGORA.</figcaption></figure>',
    '[BIO]':'<figure class="approved-bio-photo"><img src="assets/gabriel-serio.jpeg" width="1066" height="1600" loading="lazy" alt="Gabriel Quintanilha, idealizador da Advventure"></figure><div class="awards" role="region" tabindex="0" aria-label="Reconhecimento Best Lawyers de 2020 a 2026"><img src="assets/best-lawyers-2020-2026.png" width="2172" height="724" loading="lazy" alt="Sete selos Best Lawyers, de 2020 a 2026"></div>',
    '[PRECO_ABERTURA]':'<div class="installment-price"><span>Em até <b data-installments>6x</b> de</span><strong data-installment>R$ 70<sup>*</sup></strong></div><p class="cash-price">De <s data-original>R$ 600</s> por <b data-total>R$ 420</b> no Pix ou boleto.</p><p class="payment-note">*R$ 70 é uma referência provisória. O parcelamento no cartão tem juros. O valor definitivo das parcelas e o total financiado serão apresentados no checkout, conforme a opção escolhida.</p><p class="payment-note">O honorário de abertura não inclui taxas da OAB, Prefeitura e demais órgãos, cobradas à parte.</p>'}
    def inline(s):return re.sub(r'\*\*(.*?)\*\*',r'<strong>\1</strong>',html.escape(s.strip()))
    def content(s):
        result=[];listing=None
        def close():
            nonlocal listing
            if listing:result.append('</'+listing+'>');listing=None
        for block in re.split(r'\n\s*\n',s.strip()):
            block=block.strip()
            if not block:continue
            if block in markers:close();result.append(markers[block]);continue
            cta=re.fullmatch(r'\[CTA (\w+)\|(.+)\]',block)
            if cta:
                close();kind={'abertura':'opening','migracao':'migration','consultor':'consultant'}[cta[1]]
                result.append(f'<button type="button" class="cta {"outline" if kind!="opening" else ""}" data-action="{kind}">{inline(cta[2])}<span aria-hidden="true">↗</span></button>');continue
            if block.startswith('#### '):close();result.append('<h3>'+inline(block[5:])+'</h3>');continue
            if block.startswith('### '):close();result.append('<h2>'+inline(block[4:])+'</h2>');continue
            if block.startswith('- ') or re.match(r'^\d+\. ',block):
                close();kind='ul' if block.startswith('- ') else 'ol';result.append('<'+kind+' class="approved-list">')
                for line in block.splitlines():result.append('<li>'+inline(re.sub(r'^(- |\d+\. )','',line))+'</li>')
                result.append('</'+kind+'>');continue
            close();result.append('<p>'+inline(block).replace('\n','<br>')+'</p>')
        close();return ''.join(result)
    stamp='<img class="stamp" src="assets/carimbo-30-off.svg" width="320" height="320" alt="30% OFF na abertura de CNPJ">'
    new=[]
    for n,title,body in sections:
        output=content(body)
        if n==1:
            output=output.replace('<p>BLACK FRIDAY ADVVENTURE</p>','<p class="eyebrow hero-eyebrow">BLACK FRIDAY ADVVENTURE</p>',1).replace('<h2>','<h1>',1).replace('</h2>','</h1>',1)
            output=output.replace('<p><strong>Contabilidade feita para advogados, idealizada por Gabriel Quintanilha.</strong></p>','<p class="hero-proof">Contabilidade feita para advogados, idealizada por Gabriel Quintanilha.</p>')
            new.append('<section class="hero approved-hero"><div class="wrap hero-inner"><div class="hero-copy"><img class="campaign-logo" src="assets/logo-campanha.png" width="2172" height="724" alt="Black Friday 2026 Advventure Contabilidade">'+output+'</div><div class="hero-art"><div class="halo"></div><img class="gabriel-hero" src="assets/gabriel-sorriso-recortado.png" width="1024" height="1536" fetchpriority="high" alt="Gabriel Quintanilha sorrindo, com terno azul e gravata vermelha">'+stamp+'</div></div></section>');continue
        if n in (11,12):output=re.sub(r'<h3>(.*?)</h3>(.*?)(?=<h3>|$)',r'<details><summary>\1</summary>\2</details>',output,flags=re.S)
        if n==3:
            parts=output.split('<h3>',1)
            output='<div class="paths"><article><figure class="lawyer-crop before"><img src="assets/advogado-comparativo.png" width="2172" height="724" loading="lazy" alt="Profissional com documentos acumulados, imagem ilustrativa"><figcaption>IMAGEM ILUSTRATIVA</figcaption></figure>'+parts[0]+'</article><article><figure class="lawyer-crop after"><img src="assets/advogado-comparativo.png" width="2172" height="724" loading="lazy" alt="Profissional com rotina organizada, imagem ilustrativa"><figcaption>IMAGEM ILUSTRATIVA</figcaption></figure><h3>'+parts[1]+'</article></div>'
        if n==5:
            output=output.replace('<h3>Para abrir seu CNPJ</h3>','<div class="process-grid"><div><h3>Para abrir seu CNPJ</h3>').replace('<h3>Para migrar sua contabilidade</h3>','</div><div><h3>Para migrar sua contabilidade</h3>')+'</div></div>'
        if n==9:
            output=output.replace('<h3>Abertura de CNPJ — 30% OFF</h3>','<div class="offers" id="ofertas"><article class="offer primary">'+stamp+'<h3>Abertura de CNPJ — 30% OFF</h3>').replace('<h3>Migração de contabilidade — primeiro mês por nossa conta</h3>','</article><article class="offer"><h3>Migração de contabilidade — primeiro mês por nossa conta</h3>')+'</article></div>'
        if n==13:output='<div class="closing">'+stamp+output+'</div>'
        new.append(f'<section class="section approved-section {"tonal" if n%2==0 else ""}" id="bloco-{n}"><div class="wrap"><p class="eyebrow"><span>{n:02}</span> {html.escape(title)}</p><div class="approved-body">'+output+'</div></div></section>')
    doc=re.sub(r'(<main id="conteudo">).*?</main>',lambda m:m[1]+''.join(new)+'</main>',doc,flags=re.S)
    doc=re.sub(r'<p>Advventure Contabilidade<br><span>.*?</span></p>','<p>Advventure Contabilidade<br><span>Contabilidade feita para advogados, idealizada por Gabriel Quintanilha.</span></p>',doc)
    doc=re.sub('antecipada','',doc,flags=re.I).replace('SUPER BLACK FRIDAY','BLACK FRIDAY').replace('Super Black Friday','Black Friday')
    return doc.replace('<link rel="stylesheet" href="final.css">','<link rel="stylesheet" href="final.css"><link rel="stylesheet" href="approved.css">')
