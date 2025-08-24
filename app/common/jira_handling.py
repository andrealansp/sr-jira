from typing import Dict

import pandas as pd
from dotenv import load_dotenv
from jira import JIRA
from jira.resources import Issue
import logging

logger = logging.getLogger("preventivas")
load_dotenv()

class JiraHandling:
    def __init__(self, url: str, username: str, password: str, fields: str = None):
        self.__jql = ""
        self.__url = url
        self.__username = username
        self.__password = password
        self.__fields = fields
        self.__jira = JIRA(
            server=self.__url, basic_auth=(self.__username, self.__password),async_=True
        )

    def set_jql(self, escolha: str, dt_inicial: str = None, dt_final: str = None) -> None:
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
                AND created <= endOfMonth() AND "Request Type" IN ("PREVENTIVA PONTO DE COLETA (CIES)")"""

    def __repr__(self):
        return f"{self.__jql, self.__url, self.__username, self.__jql}"

    def get_all_issues(self, fields='*all') -> list[Issue] | None:
        """
        """
        issues_list = []
        try:
            for issue in self.__jira.enhanced_search_issues(self.__jql, fields=fields, maxResults=False, ):
                issues_list.append(issue)
        except Exception as e:
            print(f"Ocorreu um erro durante a busca: {e}")

        return issues_list

    def getissues(self) -> Dict[str, Issue] | None:
        """return: dict{chamado_key: {dict_issue}}"""
        try:
            issues = self.get_all_issues(self.__fields)
            dict_chamados = {}
            for issue in issues:
                dict_chamados[issue.key] = issue
            return dict_chamados
        except Exception as e:
            print(f"Erro ai camarada: {e.__str__()}")

    def getfields(self) -> list:
        fields = self.__jira.fields()
        return fields

    def getattachements(self, chave) -> Issue:
        issue = self.__jira
        attachment = issue.issue(chave, fields="attachment")
        return attachment

    def get_statistic_preventive(self) -> dict | None:
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
            logger.debug(dados_estatisticos)
            return dados_estatisticos
        else:
            return None

    def get_statistic_corrective(self) -> dict | None:
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


# if __name__ == "__main__":
#     import os
#     jira = JiraHandling(os.environ["BASE_URL"], os.environ["USER_JIRA"], os.environ["API_TOKEN"])
#     jira.set_jql("perkons-preventivas-pcls", dt_inicial="2025-01-08", dt_final="2025-12-31")
#     chamados2 = jira.get_all_issues(os.getenv("CAMPOS_PCLS"))
#     print(len(chamados2))
#     for chamado in chamados2:
#         print(chamado.fields.customfield_10117)
#         print(chamado.fields.customfield_10118.content[0].content[0].text)
#         exit()

