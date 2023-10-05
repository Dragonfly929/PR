import socket
import json
from bs4 import BeautifulSoup

HOST = '127.0.0.1'
PORT = 8080


def send_request(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    client_socket.send(f"GET {request} HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n\r\n".encode())

    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data

    client_socket.close()
    return response.decode('utf-8')


def parse_home_page(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    title = soup.find('title').text.strip()
    content = soup.find('body').text.strip()
    return {"title": title, "content": content}


def parse_about_page(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    title = soup.find('title').text.strip()
    content = soup.find('body').text.strip()
    return {"title": title, "content": content}


def parse_product_page(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    product_details = {"name": "", "author": "Author not found", "price": 0.0, "description": "Description not found"}

    title_element = soup.find('title')
    if title_element:
        product_details["name"] = title_element.text.strip()

    for p_element in soup.find_all('p'):
        p_text = p_element.text.strip()
        if p_text.startswith("Author:"):
            product_details["author"] = p_text.replace("Author:", "").strip()
        elif p_text.startswith("Price:"):
            price_text = p_text.replace("Price:", "").strip()
            try:
                product_details["price"] = float(price_text.replace('$', ''))
            except ValueError:
                product_details["price"] = 0.0
        elif p_text.startswith("Description:"):
            product_details["description"] = p_text.replace("Description:", "").strip()

    return product_details


def parse_product_listing_page(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    product_routes = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href.startswith('/product/'):
            product_routes.append(href)

    return product_routes



if __name__ == "__main__":
    pages_to_parse = ['/', '/about', '/products', '/product-listing']

    for page in pages_to_parse:
        page_content = send_request(page)
        if page == '/':
            parsed_data = parse_home_page(page_content)
        elif page == '/about':
            parsed_data = parse_about_page(page_content)
        elif page == '/products':
            parsed_data = page_content
        elif page == '/product-listing':
            product_routes = parse_product_listing_page(page_content)
            parsed_data = product_routes

        with open(f'{page.replace("/", "")}_data.json', 'w') as json_file:
            json.dump(parsed_data, json_file, indent=4)

    product_details_list = []
    for route in product_routes:
        product_page_content = send_request(route)
        product_details = parse_product_page(product_page_content)
        product_details_list.append(product_details)

        with open(f'product_{route.split("/")[-1]}_details.json', 'w') as json_file:
            json.dump(product_details, json_file, indent=4)

    print("Pages and product details saved.")
