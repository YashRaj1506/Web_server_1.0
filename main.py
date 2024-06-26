# Uncomment this to pass the first stage
import socket
import threading
import sys
import os


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")


    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(16)
    while True:
        conn, addr = server_socket.accept() # wait for client
        t = threading.Thread(target=request_handler, args=(conn,))
        t.start()
    

def request_handler(conn: socket.socket):
    while True:
        # conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 15\r\n\r\n")
        data = conn.recv(1024)
        # if not data:
        #     conn.close()
        #     return
        request_data = data.decode().split("\r\n")
        response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n"
        request_mid = request_data[0].split(" ")[1]
        request_data_2 = data.decode().split("\r\n")[0].split(" ")[1] 
        request_post_file = data.decode().split("\r\n")[0].split("/")[0]
        # if not data:
        #     break
        if request_mid == "/":
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        elif "echo" in request_mid:
            request_echo_part = request_mid.split("/")[2]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(request_echo_part)}\r\n\r\n{request_echo_part}".encode()
        
        elif request_data_2 == "/user-agent":
            
            user_agent = data.decode().split("\r\n")[2].split(":")[1].strip()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()

        elif request_mid.startswith("/files"):
            directory = sys.argv[2]
            filename = request_mid[7:]
            print(directory,filename)
            try:
                with open(f"/{directory}/{filename}", "r") as f:
                    body = f.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()  
            except Exception as e:
                response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
        elif request_post_file.strip() == "POST" and request_post_file[1] == "files":
            filename = data.decode().split("\r\n")[0].split("/")[2]
            # file_path = os.path.join(base_directory, filename)
            with open(f"{filename}", "w") as file_writable:

        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"    

        conn.sendall(response)  
        

    

    # while conn:
    #     while True:
    #         data = conn.recv(1024)
    #         request_data = data.decode().split("\r\n")
    #         response = b"HTTP/1.1 200 OK\r\n\r\n"
    #         request_mid = request_data[0].split(" ")[1]
    #         if not data:
    #             break
    #         if request_mid != "/":
    #             response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    #         if "echo" in request_mid:
    #             request_echo_part = request_mid.split("/")[2]
    #             response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(request_echo_part)}\r\n\r\n{request_echo_part}".encode()

    #         request_data_2 = data.decode().split("\r\n")[0].split(" ")[1] 
    #         if request_data_2 == "/user-agent":
    #             user_agent = data.decode().split("\r\n")[2].split(":")[1].strip()
    #             response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()


               


    #         conn.sendall(response)    



    # # server_socket.accept()[0].sendall(b"HTTP/1.1 200 OK\r\n\r\n")

    
if __name__ == "__main__":
    main()
