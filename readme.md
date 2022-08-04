# Projeto To-do list em flask

## Descrição do projeto


### Resumo


### Tecnologias e features


---
## Progresso

### Etapa 1: crud do to-do, salvar no github e deploy no heroku

- [X] Hello world em flask.
- [X] Criar modelo de tarefas.
- [X] Init db no flask shell e popular 2 tarefas para teste. 
- [X] templete q exiba as tarefas em tabela com botões (check, update, delete), tipo crud com html.
- [X] botão de adicionar tarefa no template
- [X] página com form para adicionar tarefa no banco
- [X] form na pg de To-do para adicionar tarefa no banco
- [X] função para dar "check" na tarefa, sem pg, redireciona para a lista de novo.
- [X] função para deletar a tarefa
- [X] salvar no github
- [X] apontar a home para o to-do 
- [X] deploy no heroku


### Etapa 2: Login e Admin

- [X] colocar secret key no app
- [X] instalar o flask-login na venv
- [X] instânciar login_manager
- [X] criar modelo para Usuário e herdar o user mixin
- [X] criar a função user_loader

- [X] instalar o flask-admin
- [X] instanciar Admin e configurar o app
- [X] adicionar os modelos no admin

- [X] criar um view de home separada do to-do
- [X] criar um view de login
- [X] criar uma view registro
- [X] botão de logout
- [X] hash no registro e na verificação do login

- [X] atualizar o requirements.txt
- [X] criar um relacionamento entre tarefas e usuário.
- [X] restringir o acesso do to-do para usuários logados
- [X] o add do to-do tem apontar para o dono da tarefa
- [X] Na página to-do, mostrar apenas as tarefas do usuário logado (current_user)
- [X] restringir o acesso as views do admin para usuários admin.
- [X] mudar o dunder repr de usuário para mostrar o nome e o id
- [X] adicionar o usuário logado no cabeçalho junto com um botão de logout
- [ ] colocar a máscara de e-mail no cadastro e login (atualizar e-mail do usuário admin e pelo banco)

### Etapa 3: APIS e Modulirizar a aplicação

- [X] get de todos os usuários

- [X] get de usuário por id e suas tarefas
- [ ] put de um usuário (update)
- [ ] delete de um usuário

- [ ] post de uma tarefa
- [ ] get de uma tarefa
- [ ] put de uma tarefa 
- [ ] delete\ de uma tarefa 

### Etapa 4: Extras

- [ ] completar a descrição do read.me
- [ ] testar outro framework css classless ou light weight
- [ ] deixar a forma de exibir se a tarefa está completa mais bonita