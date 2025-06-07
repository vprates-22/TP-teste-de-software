# To-Do List App

## 1. Membros do Grupo
- Victor Prates Figueiredo

## 2. Explicação do Sistema
Este é um sistema de lista de tarefas (To-Do List) onde os usuários podem:
- Criar uma conta e fazer login
- Adicionar tarefas com título, descrição, prioridade e tags personalizadas
- Marcar tarefas como concluídas ou excluí-las
- Visualizar tarefas ordenadas por prioridade (não concluídas primeiro)
- Filtrar por tags

## 3. Tecnologias Utilizadas
- Django (Python)
- SQLite3 (banco de dados padrão)
- HTML/CSS para o frontend
- GitHub Actions para CI/CD
- Coverage.py para medição da cobertura
- Codecov para publicação dos relatórios de cobertura

## 🚀 Como rodar o projeto localmente

### 1. Clone o repositório
```bash
git clone https://github.com/vprates-22/TP-teste-de-software.git
cd TP-teste-de-software
```

### 2. Crie e ative um ambiente virtual
```bash
python -m venv env
source env/bin/activate   # no Linux/macOS
env\Scripts\activate      # no Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Rode as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crie um superusuário (opcional, para admin)
```bash
python manage.py createsuperuser
```

### 6. Rode o servidor de desenvolvimento
```bash
python manage.py runserver
```

Acesse em: [http://localhost:8000](http://localhost:8000)

---

## ✅ Rodando os testes

### Com cobertura:
```bash
coverage run manage.py test
coverage report
```

### Com pytest (se estiver usando):
```bash
pytest --cov --cov-branch --cov-report=xml
```
