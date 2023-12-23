from apps.recipes.models import Recipe


def email_verify(otp):
    html_body = f"""
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {{
      font-family: 'Arial', sans-serif;
      background-color: #f4f4f4;
      text-align: center;
      padding: 20px;
    }}

    .container {{
      max-width: 400px;
      margin: 0 auto;
      background-color: #ffffff;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      border-top: 2px solid #007bff;
      border-bottom: 2px solid #007bff;
      overflow: hidden;
    }}

    h1, p, .otp, .highlight {{
      text-align: center;
    }}

    h1 {{
      color: #333333;
    }}

    p {{
      color: #666666;
      margin-bottom: 20px;
    }}

    .otp {{
      font-size: 24px;
      font-weight: bold;
      color: #007bff;
    }}

    .highlight {{
      font-weight: bold;
      color: #007bff;
    }}
  </style>
</head>

<body>
  <div class="container">
    <h1>Your Account Verification</h1>
    <p>Your One-Time Code Is</p>
    <p class="otp">{otp}</p>
    <p>This Code Is Valid For <span class="highlight">One Hour</span></p>
  </div>
</body>
</html>

    """
    return html_body


def password_reset(otp):
    html_body = f"""
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {{
      font-family: 'Arial', sans-serif;
      background-color: #f4f4f4;
      text-align: center;
      padding: 20px;
    }}

    .container {{
      max-width: 400px;
      margin: 0 auto;
      background-color: #ffffff;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      border-top: 2px solid #007bff;
      border-bottom: 2px solid #007bff;
      overflow: hidden;
    }}

    h1, p, .otp, .highlight {{
      text-align: center;
    }}

    h1 {{
      color: #333333;
    }}

    p {{
      color: #666666;
      margin-bottom: 20px;
    }}

    .otp {{
      font-size: 24px;
      font-weight: bold;
      color: #007bff;
    }}

    .highlight {{
      font-weight: bold;
      color: #007bff;
    }}
  </style>
</head>

<body>
  <div class="container">
    <h1>Password Reset For Account</h1>
    <p>Your One-Time Code Is</p>
    <p class="otp">{otp}</p>
    <p>This Code Is Valid For <span class="highlight">Ten Minutes</span></p>
  </div>
</body>
</html>

    """
    return html_body


def recipe_detail(recipe: Recipe):
    css = """
/* Reset some default styles for better consistency */
body, h1, p {
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Arial', sans-serif;
    background-color: #f4f4f4;
}

.container {
    max-width: 800px;
    margin: 20px auto;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
}

.recipe-image {
    width: 100%;
    height: auto;
}

.recipe-details {
    margin-top: 20px;
}

.recipe-title {
    font-size: 24px;
    font-weight: bold;
    color: #333;
}

.recipe-description {
    font-size: 16px;
    color: #555;
    margin-top: 10px;
}

.recipe-meta {
    margin-top: 15px;
}

.recipe-meta span {
    display: block;
    margin-bottom: 5px;
    color: #777;
}

.recipe-tags {
    margin-top: 15px;
}

.recipe-tags .tag {
    display: inline-block;
    background-color: #4caf50;
    color: #fff;
    padding: 5px 10px;
    margin-right: 5px;
    margin-bottom: 5px;
    border-radius: 5px;
    font-size: 14px;
}

.recipe-ingredients {
    margin-top: 15px;
}

.recipe-ingredients .ingredient {
    display: block;
    color: #333;
    margin-bottom: 5px;
}

.recipe-link {
    margin-top: 15px;
}

.recipe-link a {
    color: #2196f3;
    text-decoration: none;
    font-weight: bold;
}
"""

    html_body = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>{css}</style>
    <title>{recipe.title} - Recipe Details</title>
</head>
<body>

<div class="container">
    <div class="recipe-details">
        <div class="recipe-title">{recipe.title}</div>

        <div class="recipe-description">{recipe.description}</div>

        <div class="recipe-meta">
            <span>Preparation Time: {recipe.preparation_time_minutes} minutes</span>
            <span>Price: ${recipe.price}</span>
            <span>Difficulty: {recipe.get_competence_level_display()}</span>
            <span>Created At: {recipe.created_at}</span>
            <span>Updated At: {recipe.updated_at}</span>
        </div>

        <div class="recipe-tags">
            Tags:
            {" ".join(f'<span class="tag">{tag.name}</span>' for tag in recipe.tags.all())}
        </div>

        <div class="recipe-ingredients">
            Ingredients:
            {" ".join(f'<div class="ingredient">{ingredient.name}</div>' for ingredient in recipe.ingredients.all())}
        </div>

    </div>
</div>

</body>
</html>
"""
    payload = {'css': css, 'html': html_body}
    return payload
