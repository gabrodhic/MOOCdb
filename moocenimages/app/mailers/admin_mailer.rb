class AdminMailer < ActionMailer::Base
  default from: "no-reply@moocviz.csail.mit.edu"

  def new_user_waiting_for_approval(new_user)
    @new_user = new_user

    mail to: Rails.configuration.admin_email, subject: "New user for MOOCviz requires approval"
  end
end
