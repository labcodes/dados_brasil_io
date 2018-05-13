from dateutil.parser import parse
from datetime import datetime
import pandas as pd
from django.core.management import BaseCommand

from empresas.models import Empresa
from politicos.models import GastoCotaParlamentar, Deputado


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)
        parser.add_argument('inicio', type=int)

    def parse_data(self, data):
        try:
            return parse(data)
        except Exception:
            return None

    def handle(self, *args, **options):
        log = open('GASTOS_LOG.txt', 'a')

        cnpjs_salvos = list(Empresa.objects.values_list('cnpj', flat=True))
        deputados_salvos = list(Deputado.objects.values_list('id', flat=True))

        log.write(f'{datetime.now().isoformat()}  Abrindo CSV\n')
        csv = pd.read_csv(
            options['csv'],
            chunksize=100000,
            converters={
                'txtCNPJCPF': str,
            }
        )

        for contador, grupo in enumerate(csv):
            if contador >= options.get('inicio', 0):
                log.write(f'{datetime.now().isoformat()}  Importando dados do grupo {contador}\n')
                grupo = grupo[grupo['codLegislatura'] == 55]

                log.write(f'{datetime.now().isoformat()}  Criando empresas não registradas do grupo {contador}\n')
                empresas_invalidas = grupo[
                    (grupo['txtCNPJCPF'].str.len() == 14) &
                    (~grupo['txtCNPJCPF'].isin(cnpjs_salvos))
                ]
                empresas_invalidas = empresas_invalidas.drop_duplicates(['txtCNPJCPF'], keep='first')
                empresas = []
                for empresa in empresas_invalidas.itertuples():
                    empresas.append(Empresa(
                        cnpj=empresa.txtCNPJCPF,
                        nome=empresa.txtFornecedor,
                        uf_id=empresa.sgUF
                    ))
                    cnpjs_salvos.append(empresa.txtCNPJCPF)

                Empresa.objects.bulk_create(empresas)


                log.write(f'{datetime.now().isoformat()}  Criando deputados não registradas do grupo {contador}\n')
                deputados = grupo[
                    (~grupo['idecadastro'].isin(deputados_salvos))
                ]
                deputados = deputados.drop_duplicates(['idecadastro'], keep='first')
                deputados_novos = []
                for dados in deputados.itertuples():
                    deputados_novos.append(Deputado(
                        id=dados.idecadastro,
                        nome=dados.txNomeParlamentar,
                        partido_id=dados.sgPartido,
                        id_legislatura=dados.codLegislatura,
                        carteira_parlamentar=dados.nuCarteiraParlamentar,
                        uf_id=dados.sgUF,
                    ))
                    deputados_salvos.append(dados.idecadastro)

                Deputado.objects.bulk_create(deputados_novos)

                log.write(f'{datetime.now().isoformat()}  Importando gastos do grupo {contador}\n')
                gastos = []
                for dados in grupo.itertuples():
                    cnpj = dados.txtCNPJCPF if len(dados.txtCNPJCPF) == 14 else None
                    cpf = dados.txtCNPJCPF if len(dados.txtCNPJCPF) == 11 else None
                    data = self.parse_data(dados.datEmissao)
                    gastos.append(GastoCotaParlamentar(
                        deputado_id=dados.idecadastro,
                        empresa_id=cnpj,
                        cpf=cpf,
                        legislatura=dados.codLegislatura,
                        data_emissao=data,
                        id_documento=dados.ideDocumento,
                        tipo_documento=dados.indTipoDocumento,
                        ano=dados.numAno,
                        mes=dados.numMes,
                        subcota=dados.numSubCota,
                        especificacao_subcota=dados.numEspecificacaoSubCota,
                        lote=dados.numLote,
                        parcela=dados.numParcela,
                        descricao=dados.txtDescricao,
                        descricao_especificacao=dados.txtDescricaoEspecificacao,
                        fornecedor=dados.txtFornecedor,
                        numero_documento=dados.txtNumero,
                        nome_passageiro=dados.txtPassageiro,
                        trecho_viagem=dados.txtTrecho,
                        valor_documento=dados.vlrDocumento,
                        valor_glosa=dados.vlrGlosa,
                        valor_liquido=dados.vlrLiquido,
                        valor_restituicao=dados.vlrRestituicao,
                    ))

                log.write(f'{datetime.now().isoformat()}  Criando gastos do grupo {contador}\n')
                GastoCotaParlamentar.objects.bulk_create(gastos)

        log.write(f'{datetime.now().isoformat()}  Importação finalizada\n')

