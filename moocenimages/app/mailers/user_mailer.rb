class UserMailer < ActionMailer::Base
  default from: "from@example.com"

  # Subject can be set in your I18n file at config/locales/en.yml
  # with the following lookup:
  #
  #   en.user_mailer.user_approved.subject
  #
  def user_approved(user)
    @user = user

    mail to: user.email, subject: "Your MOOCviz account has been approved"
  end
end
