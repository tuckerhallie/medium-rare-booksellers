from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from views import get_single_reaction, get_single_reaction, get_all_reactions, get_all_posts, get_single_post, get_post_by_user, create_post, delete_post, get_all_post_reactions, get_single_post_reaction, create_post_reaction, delete_post_reaction
from views.user import create_user, login_user


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""
        self._set_headers(200)
        response = {}
        parsed = self.parse_url(self.path)
        
        if '?' not in self.path:
            ( resource, id ) = parsed
            if resource == "users":
                if id is not None:
                    response = get_single_user(id)
                else:
                    response = get_all_users()
            if resource == "posts":
                if id is not None:
                    response = get_single_post(id)
                else:
                    response = get_all_posts()
            if resource == "comments":
                if id is not None:
                    response = get_single_comment(id)
                else:
                    response = get_all_comments()
            if resource == "post_reactions":
                if id is not None:
                    response = get_single_post_reaction(id)
                else:
                    response = get_all_post_reactions()
                    
        else: 
            (resource, query) = parsed
            
            if query.get('posts') and resource == 'users':
                response = get_posts_by_user(query['posts'][0])
                
            if query.get('comments') and resource == 'posts':
                response = get_comments_by_post(query['comments'][0])
                
        self.wfile.write(json.dumps(response).encode())



    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        resource, _ = self.parse_url()
        
        new_post = None
        new_comment = None
        new_post_reaction = None

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)
        if resource == 'posts':
            response = create_post(post_body)
        if resource == 'comments':
            response = create_comment(post_body)
        if resource == 'post_reaction':
            response = create_post_reaction(post_body)

        self.wfile.write(response.encode())
        

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        success = False
        
        if resource == "users":
            success = update_user(id, post_body)
            
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
        self.wfile.write("".encode())


    def do_DELETE(self):
        """Handle DELETE Requests"""
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)
        
        if resource == "posts":
            delete_post(id)
            self.wfile.write("".encode())
        if resource == "comments":
            delete_comment(id)
            self.wfile.write("".encode())
        if resource == "post_reaction":
            delete_post_reaction(id)
            self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
