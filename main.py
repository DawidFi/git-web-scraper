import requests
import json

print("Welcome to the GitHub user data scraper! (Enter 'exit' to quit)")

while True:
    user_prompt = input("Enter a GitHub username: ")

    if user_prompt.lower() == "exit":
        print("Thank you for using the GitHub web scraper")
        break
    else:
        try:
            source = requests.get(f'https://api.github.com/users/{user_prompt}')
            source.raise_for_status()
            user_data = source.json()

            if 'message' in user_data and user_data['message'] == 'Not Found':
                print(f"{user_prompt} was not found on GitHub.")
            else:
                name = user_data['name']
                nickname = user_data['login']
                repos = user_data['public_repos']

                last_commit_repo = ''
                commit_source = requests.get(f'https://api.github.com/users/{user_prompt}/events')
                commit_source.raise_for_status()
                commit_data = commit_source.json()
                for event in commit_data:
                    if event['type'] == 'PushEvent':
                        last_commit_repo = event['repo']['name']
                        break

                # Create a dictionary to store the user data
                user_data = {
                    'name': name,
                    'nickname': nickname,
                    'repositories': repos,
                    'last_commit_repository': last_commit_repo
                }

                # Save the data to a JSON file
                with open(f'{user_prompt}_github_data.json', 'w') as json_file:
                    json.dump(user_data, json_file, indent=4)

                print(f'Data for {name} ({nickname}) saved to {user_prompt}_github_data.json')

        except Exception as e:
            print('Something went wrong...')
            print(e)