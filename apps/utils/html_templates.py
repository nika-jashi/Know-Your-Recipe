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
    css = """body {
  font-family: 'Arial', sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

@page {
  size: A4;
  margin: 1cm;
}

.recipe-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  width: 90%; /* Increased width */
  max-width: 1000px; /* Increased max-width */
  height: 75vh; /* Increased height */
  margin: 20px; /* Added margin for better spacing */
}

.recipe-details {
  padding: 30px;
}

.recipe-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 45px;
  color: #333;
  margin-top: 20px;
}

.description-container {
    max-width: 450px; /* Adjusted to allow dynamic line wrapping */
    margin-bottom: 40px;
}
.recipe-description {
  font-size: 18px;
  color: #555;
  line-height: 1.5; /* Improved line height for better readability */
}

.recipe-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #888;
  font-size: 16px;
  margin-top: 40px;
  
}

.recipe-tags {
  margin-top: 42px;
}

.tag {
  background-color: #3498db;
  color: #fff;
  padding: 8px 12px;
  border-radius: 5px;
  margin-right: 10px;
}

.recipe-ingredients {
  margin-top: 55px;
}

.ingredient {
  font-size: 18px;
  margin-bottom: 20px;
}

.recipe-link {
  margin-top: 25px;
  font-size: 16px;
  color: #3498db;
  text-decoration: none;
  display: inline-block;
}

.difficulty {
  margin-top: 75px;
  font-size: 18px;
  color: #888;
}

.created_at {
  color: #888;
  float: right;
}
"""

    html_body = f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>{css}</style>
  </head>
  <body>
    <div class="recipe-container">
      <div class="recipe-details">
        <div class="recipe-title">{recipe.title}</div>
        <div class="description-container">
          <div class="recipe-description">{recipe.description}</div>
        </div>
        <div class="recipe-meta">
          <div>Preparation Time: {recipe.preparation_time_minutes} m</div>
          <div>Cost: ${recipe.price}</div>
        </div>
        <div class="recipe-tags">
          {" ".join(f'<span class="tag">{tag}</span>' for tag in recipe.tags.all())}
        </div>
        <div class="recipe-ingredients">
          <div class="ingredient">Ingredients:</div>
          <ul>
            {" ".join(f'<li>{ingredient}</li>' for ingredient in recipe.ingredients.all())}
          </ul>
        </div>
        <div class="difficulty">
        Difficulty: {recipe.get_difficulty_level_display()}
        <div class="created_at">Recipe Date: {recipe.created_at.date()}</div>
        </div>
    </div>
  </body>
</html>
"""
    payload = {'css': css, 'html': html_body}
    return payload
