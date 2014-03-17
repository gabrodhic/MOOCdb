class User < ActiveRecord::Base
  # Devise modules - see https://github.com/plataformatec/devise
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :trackable, :validatable
  acts_as_authentic
  attr_accessible :username, :email, :crypted_password, :password, :password_salt, :password_confirmation, :persistence_token

  has_many :visualizations
end
