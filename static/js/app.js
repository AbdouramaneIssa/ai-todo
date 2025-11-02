// Application To-Do List - Frontend JavaScript

const todoTitle = document.getElementById('todoTitle');
const todoDescription = document.getElementById('todoDescription');
const addBtn = document.getElementById('addBtn');
const todosList = document.getElementById('todosList');
const loading = document.getElementById('loading');
const error = document.getElementById('error');

// Charger les tâches au démarrage
document.addEventListener('DOMContentLoaded', loadTodos);

// Ajouter une tâche au clic du bouton
addBtn.addEventListener('click', addTodo);

// Ajouter une tâche en appuyant sur Entrée
todoTitle.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addTodo();
    }
});

async function loadTodos() {
    try {
        loading.style.display = 'block';
        error.style.display = 'none';

        const response = await fetch('/api/todos');
        const result = await response.json();

        loading.style.display = 'none';

        if (result.success) {
            displayTodos(result.data);
        } else {
            showError('Erreur lors du chargement des tâches');
        }
    } catch (err) {
        loading.style.display = 'none';
        showError('Erreur de connexion au serveur');
        console.error(err);
    }
}

function displayTodos(todos) {
    todosList.innerHTML = '';

    if (todos.length === 0) {
        todosList.innerHTML = '<div class="empty-state">Aucune tâche pour le moment. Ajoutez-en une ! 🎉</div>';
        return;
    }

    todos.forEach(todo => {
        const todoElement = createTodoElement(todo);
        todosList.appendChild(todoElement);
    });
}

function createTodoElement(todo) {
    const div = document.createElement('div');
    div.className = `todo-item ${todo.completed ? 'completed' : ''}`;
    div.id = `todo-${todo.id}`;

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'checkbox';
    checkbox.checked = todo.completed;
    checkbox.addEventListener('change', () => toggleTodo(todo.id, checkbox.checked));

    const content = document.createElement('div');
    content.className = 'todo-content';

    const title = document.createElement('div');
    title.className = 'todo-title';
    title.textContent = todo.title;

    const description = document.createElement('div');
    description.className = 'todo-description';
    description.textContent = todo.description || '';

    if (description.textContent) {
        content.appendChild(title);
        content.appendChild(description);
    } else {
        content.appendChild(title);
    }

    const actions = document.createElement('div');
    actions.className = 'todo-actions';

    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'btn-small btn-delete';
    deleteBtn.textContent = 'Supprimer';
    deleteBtn.addEventListener('click', () => deleteTodo(todo.id));

    actions.appendChild(deleteBtn);

    div.appendChild(checkbox);
    div.appendChild(content);
    div.appendChild(actions);

    return div;
}

async function addTodo() {
    const title = todoTitle.value.trim();
    const description = todoDescription.value.trim();

    if (!title) {
        showError('Veuillez entrer un titre pour la tâche');
        return;
    }

    try {
        loading.style.display = 'block';
        error.style.display = 'none';

        const response = await fetch('/api/todos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: description || null
            })
        });

        const result = await response.json();
        loading.style.display = 'none';

        if (result.success) {
            todoTitle.value = '';
            todoDescription.value = '';
            loadTodos();
        } else {
            showError(result.error || 'Erreur lors de l\'ajout de la tâche');
        }
    } catch (err) {
        loading.style.display = 'none';
        showError('Erreur de connexion au serveur');
        console.error(err);
    }
}

async function toggleTodo(todoId, completed) {
    try {
        const response = await fetch(`/api/todos/${todoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                completed: completed
            })
        });

        const result = await response.json();

        if (!result.success) {
            showError('Erreur lors de la mise à jour de la tâche');
            loadTodos();
        }
    } catch (err) {
        showError('Erreur de connexion au serveur');
        console.error(err);
        loadTodos();
    }
}

async function deleteTodo(todoId) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette tâche ?')) {
        return;
    }

    try {
        const response = await fetch(`/api/todos/${todoId}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (result.success) {
            loadTodos();
        } else {
            showError('Erreur lors de la suppression de la tâche');
        }
    } catch (err) {
        showError('Erreur de connexion au serveur');
        console.error(err);
    }
}

function showError(message) {
    error.textContent = message;
    error.style.display = 'block';
    setTimeout(() => {
        error.style.display = 'none';
    }, 5000);
}
