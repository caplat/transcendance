NAME	= transcendence
SRCS	= ./srcs/docker-compose.yml

all: ${NAME}

${NAME}:
	docker compose -f ${SRCS} up --build -d

createvenv:
	python3 -m venv .venv

venv:
	source .venv/bin/activate

ps:
	docker compose -f ${SRCS} ps

logs:
	docker compose -f ${SRCS} logs -f --tail 5

stop:
	docker compose -f ${SRCS} stop

purgedocker:
	docker system prune -a -f

fclean: clean
	docker compose -f ${SRCS} down -v

clean:
	docker compose -f ${SRCS} down

re: fclean all