# Trabalho Prático — Testes de Componente em um Sistema de Bicicletário

## Objetivo

Neste trabalho, vocês receberão um pequeno sistema de bicicletário já implementado, contendo:

- código-fonte do subsistema;
- testes de unidade prontos;
- estrutura básica do projeto.

O trabalho de vocês será criar os **testes de componente** do sistema, utilizando `pytest`.

Os testes de componente devem verificar a colaboração real entre as classes do subsistema, cobrindo fluxos de negócio relevantes. Não é permitido transformar o trabalho em testes unitários disfarçados, nem substituir as classes internas do subsistema por mocks.

## Sistema

O sistema representa um pequeno subsistema de empréstimo de bicicletas.

As classes principais do projeto são:

- `BikeRepository`
- `RiderRepository`
- `RentalRepository`
- `HoldRepository`
- `BikeShareService`

## Regras de negócio

### Empréstimo de bicicleta
Um usuário pode retirar uma bicicleta somente se:

- o usuário existir;
- a bicicleta existir;
- o usuário não estiver bloqueado;
- o usuário estiver com a conta ativa;
- a bicicleta estiver disponível;
- o usuário tiver menos de 2 empréstimos ativos;
- a bicicleta não estiver reservada para outro usuário.

Quando o empréstimo é feito com sucesso:

- a bicicleta deixa de estar disponível;
- o empréstimo ativo é registrado;
- se o usuário tinha uma reserva para essa bicicleta, sua entrada na fila deve ser removida.

### Devolução da bicicleta
Ao devolver uma bicicleta:

- o empréstimo ativo correspondente deve existir;
- o empréstimo é encerrado;
- se não houver reserva pendente para a bicicleta, ela volta a ficar disponível;
- se houver reserva pendente, ela continua indisponível.

### Reserva
Um usuário pode reservar uma bicicleta somente se:

- o usuário existir;
- a bicicleta existir;
- o usuário não estiver bloqueado;
- o usuário estiver com a conta ativa;
- a bicicleta estiver indisponível;
- o usuário não tiver uma reserva duplicada para a mesma bicicleta;
- o usuário não for quem já está com a bicicleta emprestada.

A reserva deve respeitar a ordem de chegada.

## Tarefa

Criem os testes de componente em:

```text
tests/components/
```

Sugestão de arquivo:

```text
tests/components/test_bike_share_component.py
```

## Quantidade esperada
Espera-se entre **10 e 12 testes de componente**.

## Cenários mínimos obrigatórios

1. empréstimo com sucesso;
2. empréstimo de bicicleta inexistente;
3. empréstimo por usuário inexistente;
4. empréstimo bloqueado por conta inativa;
5. empréstimo bloqueado por usuário bloqueado;
6. empréstimo bloqueado por limite de 2 empréstimos ativos;
7. reserva com sucesso para bicicleta indisponível;
8. tentativa de reserva duplicada;
9. devolução simples sem reserva pendente;
10. devolução com reserva pendente, mantendo a bicicleta indisponível;
11. empréstimo bem-sucedido por usuário que tinha reserva para a mesma bicicleta, removendo a reserva;
12. sequência completa: empréstimo → reserva por outro usuário → devolução → tentativa de novo empréstimo.

## Requisitos de qualidade

Os testes devem:

- usar as classes reais do subsistema;
- refletir fluxos de negócio;
- ser legíveis e bem nomeados;
- evitar duplicação excessiva;
- ser determinísticos.

## Execução

Para executar os testes de unidade:

```bash
pytest tests/unit
```

Para executar todos os testes:

```bash
pytest
```
