url = "https://lilian-raillon.fr/send_mail.php"
token = "b4iQvENGdfjhF773pA7rK7WVC"
message_topic = "Bonjour,<br/><br/>Un nouveau message a été créé sur votre topic.<br/>Connectez-vous à votre compte et consultez \"Mes topics\" pour en savoir plus.<br/><br/>L'équipe Orphée"
message_account = "Bonjour,<br/><br/>Nous vous souhaitons la bienvenue sur le forum Orphée.<br/>Que vous veniez pour témoigner ou pour être témoin, nous espérons que le forum que nous avons créé vous apportera soutien et bienveillance.<br/><br/>Chaleureusement,<br/>L'Équipe Orphée"
message_delete = "Bonjour,<br/><br/>Nous sommes désolés de vous voir partir. Si vous nous avez quittés, c'est probablement que nous avons failli à notre mission. N'hésitez pas à nous faire part des points que nous pourrions améliorer sur le forum via cette adresse mail : contact@orphee.co<br/><br/>Cordialement,<br/>L'Équipe Orphée"

def message_token(token):
    return "Bonjour,<br/><br/>Voici votre token pour réinitiliser votre compte:<br/>" + token + "<br/><br/>Cordialement,<br/>L'Équipe Orphée"