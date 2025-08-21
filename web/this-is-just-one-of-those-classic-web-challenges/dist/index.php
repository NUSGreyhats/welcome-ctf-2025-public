<?php
session_start();

if (isset($_POST['action']) && $_POST['action'] == 'update_profile') {
    include 'profile.php';
}
?>

<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select, textarea { width: 100%; padding: 8px; margin-bottom: 5px; }
        button { background: #007cba; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .recommendations { margin-top: 30px; border-top: 1px solid #ccc; padding-top: 20px; }
    </style>
</head>
<body>
    <h1>Update Profile</h1>
    <form method="post">
        <input type="hidden" name="action" value="update_profile">
        
        <div class="form-group">
            <label>Email Address:</label>
            <input type="email" name="email" value="<?= $_SESSION['email'] ?? 'user@example.com' ?>">
        </div>

        <div class="form-group">
            <label>Display Name:</label>
            <input type="text" name="name" value="<?= $_SESSION['name'] ?? '' ?>" placeholder="How others see you">
        </div>

        <div class="form-group">
            <label>Age:</label>
            <input type="number" name="age" value="<?= $_SESSION['age'] ?? '25' ?>" min="13" max="120">
        </div>

        <div class="form-group">
            <label>Location:</label>
            <input type="text" name="location" value="<?= $_SESSION['location'] ?? '' ?>" placeholder="City, Country">
        </div>

        <div class="form-group">
            <label>Bio:</label>
            <textarea name="bio" rows="3" placeholder="Tell us about yourself..."><?= $_SESSION['bio'] ?? '' ?></textarea>
        </div>

        <div class="form-group">
            <label>Newsletter Preferences:</label>
            <select name="newsletter">
                <option value="weekly">Weekly Updates</option>
                <option value="monthly">Monthly Digest</option>
                <option value="none">No Emails</option>
            </select>
        </div>

        <div class="form-group">
            <label>Product Preference:</label>
            <select name="category">
                <option value="popular">Popular Items</option>
                <option value="trending">Trending Now</option>
            </select>
        </div>

        <button type="submit">Update Profile</button>
    </form>

    <?php if (isset($products)): ?>
        <div class="recommendations">
            <h3>Recommended for You:</h3>
            <?php foreach ($products as $product): ?>
                <p><?= htmlspecialchars($product['name']) ?> - $<?= $product['price'] ?></p>
            <?php endforeach; ?>
        </div>
    <?php endif; ?>
</body>
</html>