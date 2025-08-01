import os
from pprint import pprint
from typing import cast

import jirapt
import pandas as pd
from dotenv import load_dotenv
from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue

load_dotenv()

class JiraHandling:
    def __init__(self, url: str, username: str, password: str, fields: str = None):
        self.__jql = ""
        self.__url = url
        self.__username = username
        self.__password = password
        self.__fields = fields
        self.__jira = JIRA(
            server=os.getenv("BASE_URL"), basic_auth=(self.__username, self.__password)
        )

    def set_jql(self, escolha: str, dt_inicial: str = None, dt_final: str = None):
        """
        Método para definir uma variável de classe para ser utilizada pelo método search()

        :param escolha: - Escolher qual consulta realizar
        :param dt_inicial: - Data de ínicio da pesquisa.
        :param dt_final: Data final da pesquisa
        :return: Não retorna valor
        """
        match escolha:
            case "perkons-preventivas-pcls":
                self.__jql = f"""assignee IN (currentUser()) AND project = CIES AND "Request Type"
                 IN ("PREVENTIVA PONTO DE COLETA (CIES)") AND resolved >= {dt_inicial} AND resolved <= {dt_final} 
                 AND priority = Preventiva AND status = Resolved AND type = "Preventiva PCL" ORDER BY key ASC"""

            case "perkons-preventivas-salas":
                self.__jql = f"""assignee in (currentUser()) AND project = CIES AND issuetype = "Preventiva Salas"  
                AND "Request Type" in ("PREVENTIVAS SALA DE CONTROLE E OPERAÇÃO E PRODEST (CIES)") AND 
                status = Resolved AND resolved >= {dt_inicial} AND resolved <= {dt_final} ORDER BY key ASC"""

            case "perkons-corretivas-rmgv":
                self.__jql = f"""project = CIES AND issuetype IN standardIssueTypes() AND status = Resolved 
                AND assignee IN (qm:ba8a45d0-c8a8-4107-98fe-bfc59d6bde38:ba97e46a-d996-40bb-aeff-9e4d73cd3ce2,
                625768b25d1e700069aef70c, qm:ba8a45d0-c8a8-4107-98fe-bfc59d6bde38:70e33655-0037-42f7-94ef-d8503e158e39,
                currentUser()) AND type IN ("Prioridade 1", "Prioridade 2", "Prioridade 3") AND resolved >= 
                {dt_inicial} AND resolved <= {dt_final} AND "equipamentos[select list (cascading)]" IN 
                cascadeOption(10110) ORDER BY created ASC"""

            case "perkons-corretivas-fora-divisa":
                self.__jql = f"""project = CIES AND issuetype IN standardIssueTypes() AND status = Resolved AND 
                assignee IN (qm:ba8a45d0-c8a8-4107-98fe-bfc59d6bde38:ba97e46a-d996-40bb-aeff-9e4d73cd3ce2,
                625768b25d1e700069aef70c, qm:ba8a45d0-c8a8-4107-98fe-bfc59d6bde38:70e33655-0037-42f7-94ef-d8503e158e39, 
                currentUser()) AND type IN ("Prioridade 1", "Prioridade 2", "Prioridade 3") AND resolved >=
                {dt_inicial} AND resolved <= {dt_final} AND "equipamentos[select list (cascading)]" 
                IN cascadeOption(10113) ORDER BY created ASC"""

            case "velsis-preventivas-balancas":
                self.__jql = f"""project = CIES AND assignee = 625768b25d1e700069aef70c AND type = "Preventiva Balança" 
                AND status = Resolved AND created >= {dt_inicial} AND created <= {dt_final} ORDER BY created DESC"""

            case "perkons-preventivas-pcls-mes":
                self.__jql = """assignee in (currentUser()) AND project = CIES And created >= startOfMonth() 
                AND created <= now() AND "Request Type" IN ("PREVENTIVA PONTO DE COLETA (CIES)")"""

    def __repr__(self):
        return f"{self.__jql, self.__url, self.__username, self.__jql}"

    def search(self, fields):
        """
        :param fields: Lista de Campos para retorno do json
        :return: ResultList (Tipo personalizado da classe Jira)
        """
        try:
            issues = cast(
                ResultList[Issue],
                jirapt.search_issues(self.__jira, self.__jql, 4, fields=fields),
            )
            return issues
        except Exception as e:
            print(e.__str__())

    def getissues(self):
        try:
            issues = self.search(self.__fields)
            dict_chamados = {}
            for issue in issues:
                dict_chamados[issue.key] = issue
            return dict_chamados
        except Exception as e:
            print(f"Erro ai camarada: {e.__str__()}")

    def getfields(self) -> list:
        fields = self.__jira.fields()
        return fields

    def getattachements(self, chave):
        issue = self.__jira
        attachment = issue.issue(chave, fields="attachment")
        return attachment

    def get_statistic_preventive(self):
        issues = self.getissues()
        list_preventive: list = []
        for issue in issues.values():
            list_preventive.append(
                {
                    "key": issue.key,
                    "status": issue.fields.customfield_10010.currentStatus.status,
                    "regiao": issue.fields.customfield_10060.value,
                }
            )

        if list_preventive:
            df = pd.DataFrame(list_preventive)

            dados_estatisticos: dict = {
                "ABERTOS_RMGV": len(
                    df.loc[
                        (df["regiao"] == "RMGV/Divisa")
                        & (df["status"] == "Work in progress")
                    ]
                ),
                "ABERTOS_FORA_DIVISA": len(
                    df.loc[
                        (df["regiao"] == "Fora Divisa")
                        & (df["status"] == "Work in progress")
                    ]
                ),
                "FECHADOS_RMGV": len(
                    df.loc[
                        (df["regiao"] == "RMGV/Divisa") & (df["status"] == "Resolvido")
                    ]
                ),
                "FECHADOS_FORA_DIVISA": len(
                    df.loc[
                        (df["regiao"] == "Fora Divisa") & (df["status"] == "Resolvido")
                    ]
                ),
                "CHAMADOS_ABERTOS": len(df.loc[df["status"] == "Work in progress"]),
                "TOTAL_DE_CHAMADOS": len(df["status"]),
            }

            return dados_estatisticos
        else:
            return None

    def get_statistic_corrective(self):
        issues = self.getissues()
        list_corrective: list = []
        for corrective in issues.values():
            list_corrective.append(
                {
                    "chave": corrective.key,
                    "prioridade": corrective.fields.priority,
                    "atendimento": corrective.fields.customfield_10062.completedCycles[
                        0
                    ].breached,
                    "solucao": corrective.fields.customfield_10063.completedCycles[
                        0
                    ].breached,
                }
            )

        if list_corrective:
            df = pd.DataFrame(list_corrective)
            df["prioridade"] = df["prioridade"].astype(str)

            dados_estatisticos: dict = {
                "solucao_no_prazo_p1": len(
                    df.loc[
                        (df["prioridade"] == "Prioridade 1") & (df["solucao"] == False)
                    ]
                ),
                "solucao_fora_prazo_p1": len(
                    df.loc[
                        (df["prioridade"] == "Prioridade 1") & (df["solucao"] == True)
                    ]
                ),
                "solucao_no_prazo_p2": len(
                    df.loc[
                        (df["prioridade"] == "Prioridade 2") & (df["solucao"] == False)
                    ]
                ),
                "solucao_fora_prazo_p2": len(
                    df.loc[
                        (df["prioridade"] == "Prioridade 2") & (df["solucao"] == True)
                    ]
                ),
                "solucao_no_prazo_p3": len(
                    df.loc[
                        (df["prioridade"] == "Prioridade 3") & (df["solucao"] == False)
                    ]
                ),
                "solucao_fora_prazo_p3": len(
                    df.loc[
                        (df["prioridade"] == "Prioridade 3") & (df["solucao"] == True)
                    ]
                ),
                "atendimento_no_prazo_p1": len(
                    df.loc[
                        (df["prioridade"] == "Prioridade 1")
                        & (df["atendimento"] == False)
                    ]
                ),
                "atendimento_fora_prazo_p1": len(
                    df.loc[
                        (df["prioridade"] == "Prioridade 1")
                        & (df["atendimento"] == True)
                    ]
                ),
                "atendimento_no_prazo_p2": len(
                    df.loc[
                        (df["prioridade"] == "Prioridade 2")
                        & (df["atendimento"] == False)
                    ]
                ),
                "atendimento_fora_prazo_p2": len(
                    df.loc[
                        (df["prioridade"] == "Prioridade 2")
                        & (df["atendimento"] == True)
                    ]
                ),
                "atendimento_no_prazo_p3": len(
                    df.loc[
                        (df["prioridade"] == "Prioridade 3")
                        & (df["atendimento"] == False)
                    ]
                ),
                "atendimento_fora_prazo_p3": len(
                    df.loc[
                        (df["prioridade"] == "Prioridade 3")
                        & (df["atendimento"] == True)
                    ]
                ),
            }
            return dados_estatisticos
        else:
            return None


if __name__ == "__main__":
    jira = JiraHandling(os.environ["URL"], os.environ["USER_JIRA"], os.environ["API_TOKEN"])
    jira.set_jql("perkons-corretivas-rmgv","2025-07-01", dt_final="2025-08-01")
    chamados = jira.get_statistic_corrective()
    for chamado in chamados:
        print(chamado)

