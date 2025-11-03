# challenge-favorite-products

## Índice

- Meu entendimento sobre o desafio:
- Como executar o projeto
- Como testar
- Possíveis melhorias
- Desenho da solução

### Meu entendimento sobre o desafio:
Eu tinha que criar uma API para criar, atualizar, visualizar e remover clientes e também permitir o cliente criar uma lista de favoritos.

Entendi que a API de produtos que eu deveria consultar era um outro microsserviço de API, o qual eu desenvolvi uma fake api para me auxiliar, essa eu criei de forma simplificada.

Também entendi que era necessário um endpoint para, dado o id de um cliente, eu trazer todos os seus produtos favoritos e as características desses produtos, presentes na api de produtos, no meu caso a fake api.
Para isso eu criei uma rota com características de BFF para devolver essas informações.

Como o enunciado também falava sobre um auto volume de requisições, eu apliquei cache em todos os lugares que achei pertinente, como por exemplo: validar se um email já existe.

Também apliquei um sistema de fila e job para o endpoint que vincula um produto favorito a um cliente, isso porque acredito que este teria um maior volume de requisições e também porque depende de um serviço terceiro o qual não tenho controle, sendo assim ele pode estar indisponível em algum momento, e com um sistema de filas é possível sobrecarregar menos esse sistema e ter melhor controle para reprocessar se necessário.

### Desenho da solução
![System Design](./docs/system-design.png)

### Como executar o projeto

O projeto conta com um arquivo Make que ira lhe auxiliar e também todo o sistema configurado com Docker e Docker Compose.

*Importante:*

- Verifique se já não a sistemas rodando nas mesmas portas que os quais usei, para isso você pode consultar os arquivos .env e docker-compose.yml
- Os comando iram subir alguns dockers então você precisa ter os requisitos para isso instalados

*Aviso:* Caso queiram modificar o enderço da fake api product basta ir no arquivo .env e modificar o valor de `PRODUCT_API_URL`

Passo a passo executando no seu terminal:
```bash
# Passo 1
make create-env

# Passo 2
make run-build-containers

# Passo 3
make run-containers
```

Com isso agora você pode acessar as seguintes urls para testar o projecto:

Favorite Products API -> http://localhost:8000/docs
Fake Products API -> http://localhost:8001/docs

Caso queria modificar algum valor dos dados da Fake Products API você pode ir em: `app/presentation/fake_api_products/database.py`

### Como testar

Para cadastrar clientes e produtos favoritos de cliente você deve antes se autenticar.
Para isso pegue a sua chave de api do arquivo .env na variavel `API_TOKEN`.
Com o token em mãos você vai até a documentação Openapi e envia a requisição na rota `/v1/auth/token` colocando o valor de `API_TOKEN` na chave `token` no corpo da requisição.
A sua request deve ficar como essa de exemplo:
```bash
curl -X 'POST' \
  'http://localhost:8000/v1/auth/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "token": "API_TOKEN_AQUI"
}'
```
Após enviar a requisição você recebera de volta um `access_token` copie ele e cole na sessão de authorize da documentação (O botão fica no canto superior direito da documentação)
Agora você está autenticado e suas proximas requisições devem ficar como a de exemplo:
```bash
curl -X 'POST' \
  'http://localhost:8000/v1/customers' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer ACCESS_TOKEN \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Example",
  "email": "example@example.com"
}'
```
### Possíveis melhorias
Acredito que há algumas possíveis melhorias no projeto, segue uma lista de coisas que poderiam ser aplicadas:

- Concorrencia:
Podem utilizar lock no Redis para controlar alguns itens que têm alta concorrência, exemplo caso tenhamos um número muito alto de tentativas de cadastrar o mesmo e-mail.
- Dead Letter Queue(DLQ):
Podemos configurar uma DLQ para caso o serviço de API de produtos esteja fora, assim teríamos uma maneira de reprocessar.
- Arquitetura e injeção de dependencia:
O design desse projeto baseia-se em projetos nos quais já tive a experiência de trabalhar, mas sei que há algumas coisas da maneira como ele está estruturado que poderiam ser mais simples ou até mais completas, como por exemplo: melhorar a injeção de dependência, aplicando em mais pontos do sistema.
- Testes:
Apliquei teste em pontos os quais eu acredito que seria possivel mostrar o meu conhecimento em trabalhar com testes, mas eles poderiam estar aplicados em mais partes do sistema.
- Infraestrutura:
Em um cenário real, o sistema deve conter uma aplicação de load balancer na frente das APIs.
APIs e Workers devem ter no mínimo 2 instâncias e estar configuradas com um sistema de Auto Scalling.
O Redis deve estar em um cluster de Redis.
O bando de dados deve ter uma versão de escrita e uma réplica para leitura.
