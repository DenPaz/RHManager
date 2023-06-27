from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import (
    Curso,
    CursoCivil,
    CursoPM,
    FormacaoAcademica,
    LinguaEstrangeira,
    TipoAfastamento,
    TipoRestricao,
)

model_default_values = {
    LinguaEstrangeira: [
        "Alemão",
        "Árabe",
        "Espanhol",
        "Francês",
        "Hindi",
        "Inglês",
        "Italiano",
        "Japonês",
        "Mandarim",
        "Português",
        "Russo",
    ],
    FormacaoAcademica: [
        "Administração",
        "Advocacia",
        "Arquitetura e Urbanismo",
        "Biologia",
        "Ciências Contábeis",
        "Ciências Econômicas",
        "Direito",
        "Educação Física",
        "Enfermagem",
        "Engenharias",
        "Engenharia Agronômica",
        "Engenharia Ambiental",
        "Engenharia Civil",
        "Engenharia de Produção",
        "Engenharia Elétrica",
        "Engenharia Mecânica",
        "Farmácia",
        "Fisioterapia",
        "Geografia",
        "História",
        "Letras",
        "Medicina",
        "Pedagogia",
        "Psicologia",
        "Química",
        "Serviço Social",
        "Sociologia",
        "Tecnologia da Informação",
        "Veterinária",
        "Zootecnia",
    ],
    Curso: [
        "Adobe Photoshop",
        "Análise de Dados",
        "AutoCAD",
        "Design Gráfico",
        "Edição de Vídeo",
        "Escrita Criativa",
        "Excel Avançado",
        "Fotografia Digital",
        "Gestão de Projetos",
        "Ilustração Digital",
        "Inglês para Negócios",
        "Introdução à Programação",
        "Marketing Digital",
        "Microsoft Power BI",
        "Negociação e Vendas",
        "Oratória",
        "Premiere Pro",
        "Programação Web",
        "Redação Empresarial",
        "SEO e SEM",
        "Social Media Marketing",
        "SQL Básico",
        "Tableau",
        "UX/UI Design",
        "Vendas Online",
        "Web Design",
        "Wordpress",
        "Desenvolvimento em Python",
        "Gestão de Recursos Humanos",
        "Inteligência Emocional no Trabalho",
    ],
    CursoCivil: [
        "Acidentes de Trânsito e Perícia",
        "Análise Criminal",
        "Atendimento ao Público",
        "Balística Forense",
        "Crimes Cibernéticos",
        "Crimes Financeiros e Econômicos",
        "Direito Penal e Processual Penal",
        "Entrevista e Interrogatório",
        "Estatística Aplicada à Segurança Pública",
        "Estudos sobre Drogas",
        "Gestão de Crises e Negociação",
        "Investigação de Homicídios",
        "Legislação de Trânsito",
        "Medicina Legal",
        "Operações Táticas",
        "Psicologia Criminal",
        "Segurança Pública",
        "Técnicas de Investigação",
        "Tiro Policial",
        "Uso Progressivo da Força",
    ],
    CursoPM: [
        "Curso de Ações Táticas Especiais",
        "Curso de Choque",
        "Curso de Operações Especiais",
        "Curso de Formação de Oficiais",
        "Curso de Formação de Sargentos",
        "Curso de Formação de Cabos",
        "Curso de Direitos Humanos",
        "Curso Superior de Polícia",
        "Curso de Negociação de Crises",
        "Curso de Técnicas e Táticas Defensivas",
        "Curso de Operações de Controle de Distúrbios",
        "Curso de Tiro Defensivo",
        "Curso de Policiamento de Trânsito",
        "Curso de Policiamento Comunitário",
        "Curso de Policiamento Ambiental",
        "Curso de Policiamento Montado",
        "Curso de Operações em Áreas de Selva",
        "Curso de Operações em Áreas de Caatinga",
        "Curso de Operações em Áreas de Pantanal",
        "Curso de Operações em Áreas Urbanas",
    ],
    TipoAfastamento: [
        "Afastamento para Tratamento de Saúde",
        "Licença Médica",
        "Licença Maternidade",
        "Licença Paternidade",
        "Licença para Estudo",
        "Licença por Motivo de Doença em Pessoa da Família",
        "Licença para Serviço Militar",
        "Licença para Atividade Política",
        "Licença para Tratar de Interesses Particulares",
        "Licença para Desempenho de Mandato Classista",
        "Licença Prêmio por Assiduidade",
        "Licença por Acidente em Serviço",
        "Licença para Capacitação",
        "Afastamento para Cumprir Missão ou Estudo no Exterior",
        "Afastamento para Exercício de Mandato Eletivo",
        "Afastamento para Servir em Organismo Internacional",
        "Afastamento por Conveniência do Serviço",
        "Suspensão Disciplinar",
    ],
    TipoRestricao: [
        "Restrição Física",
        "Restrição Médica",
        "Restrição Psicológica",
        "Restrição Disciplinar",
        "Restrição por Inquérito",
        "Restrição Operacional",
        "Restrição de Uso de Arma",
    ],
}


@receiver(post_migrate)
def populate_default_values(sender, **kwargs):
    for model, values in model_default_values.items():
        for value in values:
            instance = model(label=value)
            instance.clean()
            model.objects.get_or_create(label=instance.label)
