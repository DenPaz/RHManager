from django.db import models


class Genero(models.TextChoices):
    MASCULINO = "M", "Masculino"
    FEMININO = "F", "Feminino"


class Comportamento(models.TextChoices):
    EXCEPCIONAL = 3, "Excepcional"
    OTIMO = 2, "Ótimo"
    BOM = 1, "Bom"
    RUIM = 0, "Ruim"


class Estado(models.TextChoices):
    AC = "AC", "Acre"
    AL = "AL", "Alagoas"
    AP = "AP", "Amapá"
    AM = "AM", "Amazonas"
    BA = "BA", "Bahia"
    CE = "CE", "Ceará"
    DF = "DF", "Distrito Federal"
    ES = "ES", "Espírito Santo"
    GO = "GO", "Goiás"
    MA = "MA", "Maranhão"
    MT = "MT", "Mato Grosso"
    MS = "MS", "Mato Grosso do Sul"
    MG = "MG", "Minas Gerais"
    PA = "PA", "Pará"
    PB = "PB", "Paraíba"
    PR = "PR", "Paraná"
    PE = "PE", "Pernambuco"
    PI = "PI", "Piauí"
    RJ = "RJ", "Rio de Janeiro"
    RN = "RN", "Rio Grande do Norte"
    RS = "RS", "Rio Grande do Sul"
    RO = "RO", "Rondônia"
    RR = "RR", "Roraima"
    SC = "SC", "Santa Catarina"
    SP = "SP", "São Paulo"
    SE = "SE", "Sergipe"
    TO = "TO", "Tocantins"


class TipoSanguineo(models.TextChoices):
    A_POSITIVO = "A+", "A+"
    A_NEGATIVO = "A-", "A-"
    B_POSITIVO = "B+", "B+"
    B_NEGATIVO = "B-", "B-"
    AB_POSITIVO = "AB+", "AB+"
    AB_NEGATIVO = "AB-", "AB-"
    O_POSITIVO = "O+", "O+"
    O_NEGATIVO = "O-", "O-"


class TipoTrabalhoAnterior(models.TextChoices):
    PRIVADO = 1, "Privado"
    MILITAR_FEDERAL = 2, "Federal (militar)"
    PUBLICO_SC = 3, "Público em SC (não militar)"
    PUBLICO_SC_MILITAR = 4, "Público em SC (militar)"
    PUBLICO_OUTRO = 5, "Público em outro estado (não militar)"
    PUBLICO_OUTRO_MILITAR = 6, "Público em outros estados (militar)"
