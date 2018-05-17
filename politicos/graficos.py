import matplotlib.pylab as plt

from politicos.models import Deputado

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def graficos_gasto_mensal():
    media_mensal = Deputado.objects.get_media_mensal()

    dados = sorted(media_mensal.items())

    eixo_x = ['/'.join(dado[0].split('_')[1:3]) for dado in dados]
    eixo_y = [dado[1] if dado[1] else 0 for dado in dados]

    return zip(chunks(eixo_x, 12), chunks(eixo_y, 12))
