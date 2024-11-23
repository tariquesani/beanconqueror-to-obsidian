import json
import os
import yaml
from datetime import datetime

# Load the configuration from config.yaml
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Extract configuration details
json_file = config['json_file']
output_dir = config['output_dir']
properties = config['properties']

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Function to sanitize file names


def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in " ._-").rstrip()

# Function to format date


def format_date(date_str):
    try:
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return date_str

# Function to generate daily note link based on a date string


def generate_daily_note_link(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    # date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    year = date_obj.strftime('%Y')
    month_num = date_obj.strftime('%m')
    month_name = date_obj.strftime('%B')
    day_date = date_obj.strftime('%Y-%m-%d')
    day_name = date_obj.strftime('%A')
    return f"/DailyNotes/{year}/{month_num}-{month_name}/{day_date}-{day_name}.md"

# Function to properly capitalise strings


def format_string(s):
    return ' '.join(word.capitalize() for word in s.split('_'))

# Function to convery bool to symbols


def format_bool(value):
    return '✓' if value else '✗'


# Function to create markdown content for a bean
def create_markdown(bean):
    content = []
    yaml_frontmatter = []

    # Process each property based on the configuration
    if properties.get('name', False):
        name = bean.get('name', 'Unnamed Bean')
        yaml_frontmatter.append(f'name: "{name}"')
        content.append(f"# {name}")

    if properties.get('roaster', False):
        roaster = bean.get('roaster', 'Unknown Roaster')
        yaml_frontmatter.append(f'roaster: "{roaster}"')
        content.append(f"**Roaster:** {roaster}")

    if properties.get('roasting_date', False):
        roasting_date = format_date(bean.get('roastingDate', ''))
        if roasting_date != '':
            yaml_frontmatter.append(f'roasting_date: "{roasting_date}"')
            daily_note_link = generate_daily_note_link(roasting_date)
            content.append(f"**Roasting Date:** [{roasting_date}]({daily_note_link})")

    if properties.get('open_date', False):
        open_date = format_date(bean.get('openDate', ''))
        if open_date != '':
            yaml_frontmatter.append(f'open_date: "{open_date}"')
            daily_note_link = generate_daily_note_link(open_date)
            content.append(f"**Opening Date:** [{open_date}]({daily_note_link})")

    if properties.get('note', False):
        note = bean.get('note', 'No Notes')
        content.append(f"## Notes\n{note}")

    if properties.get('aromatics', False):
        aromatics = bean.get('aromatics', 'No Aromatics Info')
        content.append(f"**Aromatics:** {aromatics}")

    if properties.get('weight', False):
        weight = bean.get('weight', 'Unknown Weight')
        yaml_frontmatter.append(f'weight: {weight}g')
        content.append(f"**Weight:** {weight}g")

    if properties.get('cost', False):
        cost = bean.get('cost', 'Unknown Cost')
        yaml_frontmatter.append(f'cost: ₹{cost}')
        content.append(f"**Cost:** ₹{cost}")

    if properties.get('rating', False):
        rating = bean.get('rating', 'No Rating')
        yaml_frontmatter.append(f'rating: {rating}/5')
        content.append(f"**Rating:** {rating}/5")

    if properties.get('favourite', False):
        favourite = bean.get('favourite', False)
        yaml_frontmatter.append(f'favourite: {favourite}')
        content.append(f"**Favourite:** {format_bool(favourite)}")

    if properties.get('finished', False):
        finished = bean.get('finished', False)
        yaml_frontmatter.append(f'finished: {finished}')
        content.append(f"**Finished:** {format_bool(finished)}")

    if properties.get('decaffeinated', False):
        decaffeinated = bean.get('decaffeinated', False)
        yaml_frontmatter.append(f'decaffeinated: {decaffeinated}')
        content.append(f"**Decaffeinated:** {format_bool(decaffeinated)}")

    if properties.get('roast', False):
        roast = format_string(bean.get('roast', 'Unknown'))
        yaml_frontmatter.append(f'roast: "{roast}"')
        content.append(f"**Roast Level:** {roast}")

    if properties.get('roast_range', False):
        roast_range = bean.get('roast_range', 0)
        yaml_frontmatter.append(f'roast_range: {roast_range}')
        content.append(f"**Roast Range:** {roast_range}")

    if properties.get('bean_mix', False):
        bean_mix = format_string(bean.get('beanMix', 'Unknown'))
        yaml_frontmatter.append(f'bean_mix: "{bean_mix}"')
        content.append(f"**Bean Mix:** {bean_mix}")

    if properties.get('attachments', False):
        attachments = bean.get('attachments', [])
        if attachments:
            image_path = f"photos/beans/{os.path.basename(attachments[0])}"
            yaml_frontmatter.append(f'poster: "[[{image_path}]]"')
            content.append(f"![Bean Image]({image_path})")

    # Combine YAML frontmatter and content
    yaml_section = "---\n" + \
        "\n".join(yaml_frontmatter) + "\ntags:\n - Coffee/Bean\n---\n\n"
    markdown_content = yaml_section + "\n".join(content)

    return markdown_content


# Read the JSON file
with open(json_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Process each bean and create a markdown file
for bean in data.get('BEANS', []):
    print(f"Processing {bean.get('name', 'Unnamed Bean')}...")
    bean_name = sanitize_filename(bean.get('name', 'Unnamed Bean'))
    markdown_content = create_markdown(bean)
    markdown_file = os.path.join(output_dir, f"{bean_name}.md")

    with open(markdown_file, 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_content)

print(f"Markdown files created in '{output_dir}' directory.")
