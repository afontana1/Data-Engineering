from email_validator import EmailValidator


def test_can_get_body_from_s3():
    pass


def test_can_process_body():
    validator = EmailValidator()
    validator.process_mail_body("test_data/test_email")
