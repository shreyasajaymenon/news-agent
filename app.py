import pandas as pd
import os

from agent import generate_news_prompt
from critic_agent import improve_prompt
from image_generator import generate_image


MODELS = {
    "gpt": "gpt",
    "flux": "flux",
    "sdxl": "sdxl"
}

def run_all_models(prompt, article_num):

    for model_name, model_id in MODELS.items():

        print(
            f"\nGenerating with "
            f"{model_name.upper()}..."
        )

        print("MODEL:", model_id)

        generate_image(
            prompt=prompt,
            model=model_id,
            model_name=model_name,
            article_num=article_num
        )

def process_single_news():

    news = input(
        "\nEnter news:\n\n"
    )

    print("\nCreating prompt...")

    prompt = generate_news_prompt(
        news
    )

    better_prompt = improve_prompt(
        prompt
    )

    print("\nGenerating 3 images...\n")

    run_all_models(
        better_prompt,
        article_num=1
    )


def process_csv():

    csv_path = input(
        "\nEnter CSV path:\n"
    ).strip()

    if not os.path.exists(csv_path):
        print("File not found")
        return

    df = pd.read_csv(csv_path)

    print("\nColumns found:")
    print(df.columns.tolist())

    headline_col = input(
        "\nHeadline column: "
    )

    article_col = input(
        "\nArticle column: "
    )

    print("""
Choose Selection Mode:

1. First N articles
2. Search by keyword/company
3. Pick article manually
""")

    selection = input("Choice: ")

    # OPTION 1
    if selection == "1":

        limit = int(
            input(
                "\nHow many articles?: "
            )
        )

        selected_df = df.head(limit)

    # OPTION 2
    elif selection == "2":

        keyword = input(
            "\nEnter company/keyword:\n"
        ).lower()

        filtered_df = df[
            df[headline_col]
            .str.lower()
            .str.contains(keyword, na=False)
        ]

        if filtered_df.empty:
            print(
                "No matching news found."
            )
            return

        print(
            f"\nFound "
            f"{len(filtered_df)} articles"
        )

        for idx, row in (
            filtered_df.head(10)
            .iterrows()
        ):
            print(
                f"\n[{idx}] "
                f"{row[headline_col]}"
            )

        limit = int(input(
            "\nHow many to process?: "
        ))

        selected_df = (
            filtered_df.head(limit)
        )

    # OPTION 3
    elif selection == "3":

        for idx, row in (
            df.head(20).iterrows()
        ):
            print(
                f"\n[{idx}] "
                f"{row[headline_col]}"
            )

        article_index = int(
            input(
                "\nChoose article number: "
            )
        )

        selected_df = (
            df.iloc[[article_index]]
        )

    else:
        print("Invalid option")
        return

    # PROCESS NEWS
    for idx, row in (
        selected_df.iterrows()
    ):

        print("\n" + "=" * 50)
        print(
            f"Processing article "
            f"{idx}"
        )

        headline = str(
            row[headline_col]
        )

        article = str(
            row[article_col]
        )

        print("\nHeadline:")
        print(headline)

        news_text = f"""
        Headline:
        {headline}

        Article:
        {article}
        """

        print(
            "\nGenerating prompt..."
        )

        prompt = generate_news_prompt(
            news_text
        )

        better_prompt = improve_prompt(
            prompt
        )

        print(
            "\nGenerating "
            "3 model images..."
        )

        run_all_models(
            better_prompt,
            article_num=idx
        )

    print("\nDone!")


print("""
=== NEWS IMAGE AGENT ===

1. Single News
2. CSV File
""")

choice = input(
    "\nChoice: "
)

if choice == "1":
    process_single_news()

elif choice == "2":
    process_csv()

else:
    print("Invalid choice")