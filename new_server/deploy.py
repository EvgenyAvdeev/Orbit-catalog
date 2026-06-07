import fire
from conf_info import SERVER_HOST, SERVER_PORT, SERVER_USER, SUDO_PASSWORD
from fabric import Connection
from invoke.watchers import Responder

sudo_responder = Responder(
    pattern=r"\[sudo\] password for .*:", response=f"{SUDO_PASSWORD}\n"
)


def create_conn():
    conn = Connection(
        host=SERVER_HOST,
        user=SERVER_USER,
        port=SERVER_PORT,
        connect_kwargs={"password": SUDO_PASSWORD},
    )
    return conn


def rebuild_container():
    conn = create_conn()
    with conn.cd("test/backend_repo/new_server"):
        result = conn.run(
            "sudo -S docker compose up --build -d", pty=True, watchers=[sudo_responder]
        )
    conn.close()


def use_cli(cmd: str):
    conn = create_conn()
    result = conn.run(
        f"sudo docker exec -it backend python CLI.py {cmd}",
        pty=True,
        watchers=[sudo_responder],
    )
    conn.close()


def git_pull():
    conn = create_conn()
    with conn.cd("test/backend_repo"):
        result = conn.run("git pull", pty=True, watchers=[sudo_responder])
    conn.close()


def clear_redis():
    conn = create_conn()
    result = conn.run(
        "sudo docker exec -it redis redis-cli FLUSHDB",
        pty=True,
        watchers=[sudo_responder],
    )
    conn.close()


if __name__ == "__main__":
    # bad = []
    # tags = [
    #     # "L2.H_s",
    #     "L2.H_n",
    #     # "L1.V",
    #     "L2.V",
    #     # "L1.L",
    #     # "L2.L",
    #     # "L1.H_n.2P2", новый тег
    #     "L2.L.2P1",
    #     #"L1.H_n.3P1",
    #     #"L1.H_n.3P2",
    #     #"L1.H_n.3P3",
    #     #"L1.H_n.4P1",
    #     #"L1.H_s.2P3",
    #     #"L1.H_s.3P1",
    #     #"L1.H_s.3P2",
    #     #"L1.H_s.3P3",
    #     #"L1.H_s.4P1",
    #     #"L1.L.4P1",
    #     "L2.H_n.2P2",
    #     "L2.H_n.3P1",
    #     "L2.H_s.2P1",
    #     "L2.H_s.3P1",
    #     "L2.Planar.2P1.3P1",
    #     "L2.Planar.2P1.3P2",
    # ]
    # for tag in tags:
    #     try:
    #         use_cli(f"load-family {tag}")
    #     except:
    #         bad.append(tag)
    # git_pull()
    #use_cli("get-families")
    #use_cli("load-family L1.H_n.2P2")
    #git_pull()
    rebuild_container()
    clear_redis()
    #print(bad)
