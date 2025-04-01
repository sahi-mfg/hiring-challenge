import csv
import json
import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()


def initialize_driver():
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")
    return driver


def login_to_linkedin(driver):
    username = os.getenv("LINKEDIN_USERNAME")
    password = os.getenv("LINKEDIN_PASSWORD")

    if not username or not password:
        raise ValueError("Les identifiants LinkedIn ne sont pas définis.")

    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    time.sleep(5)


def search_posts(driver, keyword):
    search_box = driver.find_element(By.XPATH, "//input[@placeholder='Recherche']")
    search_box.click()
    search_box.clear()
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

    filter_button = driver.find_element(
        By.XPATH, ".//button[@aria-pressed='false'][normalize-space()='Posts']"
    )
    filter_button.click()
    time.sleep(5)


def extract_post_data(driver, keyword):
    posts = driver.find_elements(
        By.XPATH,
        "//div[contains(@class, 'feed-shared-update-v2') and not(contains(@class, 'feed-shared-update-v2--empty'))]",
    )
    print(f"Nombre de posts trouvés: {len(posts)}")
    print(posts)
    if not posts:
        print("Aucun post trouvé.")
        return []
    time.sleep(5)

    data = []
    for post in posts:
        try:
            author_element = post.find_element(
                By.CLASS_NAME, "update-components-actor__title"
            )
            author = author_element.text if author_element else "N/A"

            print(f"Auteur: {author}")

            content_element = post.find_element(
                By.CLASS_NAME,
                "span",
            )
            content = content_element.text if content_element else "N/A"
            print(f"Contenu: {content}")

            date_element = post.find_element(
                By.CLASS_NAME,
                "update-components-actor__sub-description text-body-xsmall t-black--light",
            )
            date = date_element.text if date_element else "N/A"

            link_element = post.find_element(
                By.XPATH, ".//button[@aria-label='Copier le lien vers le post']"
            )
            link = link_element.get_attribute("href") if link_element else "N/A"

            data.append({
                "Auteur": author,
                "Date": date,
                "Contenu": content,
                "Lien": link,
                "Mot-clé": keyword,
            })
        except Exception as e:
            print(f"Erreur lors de l'extraction du post: {e}")

    return data


def save_to_csv(data, filename="linkedin_posts.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    print(f"Données enregistrées dans {filename}")


def save_to_json(data, filename="linkedin_posts.json"):
    with open(filename, mode="w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Données enregistrées dans {filename}")


def main():
    keywords = ["cybersécurité Afrique"]
    driver = initialize_driver()
    login_to_linkedin(driver)

    for keyword in keywords:
        search_posts(driver, keyword)
        posts_data = extract_post_data(driver, keyword)
        for post in posts_data:
            print(post)

    driver.quit()


if __name__ == "__main__":
    main()
