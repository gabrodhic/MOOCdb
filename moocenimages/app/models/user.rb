class User < ActiveRecord::Base
  # Devise modules - see https://github.com/plataformatec/devise
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :trackable, :validatable
  acts_as_authentic
  attr_accessible :username, :email, :crypted_password, :password, :password_salt, :password_confirmation, :persistence_token

  after_create :send_admin_new_user_email

  has_many :visualizations

  # override for user approval
  def active_for_authentication?
    super && approved?
  end

  # override for user approval
  def inactive_message
    if !approved?
      :not_approved
    else
      super # Use whatever other message
    end
  end

  # only lets user reset password if approved
  def self.send_reset_password_instructions(attributes={})
    recoverable = find_or_initialize_with_errors(reset_password_keys, attributes, :not_found)
    if !recoverable.approved?
      recoverable.errors[:base] << I18n.t("devise.failure.not_approved")
    elsif recoverable.persisted?
      recoverable.send_reset_password_instructions
    end
    recoverable
  end

  def send_admin_new_user_email
    AdminMailer.new_user_waiting_for_approval(self).deliver
  end
end
