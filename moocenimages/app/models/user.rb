class User < ActiveRecord::Base
  acts_as_authentic
  attr_accessible :username, :email, :crypted_password, :password, :password_salt, :password_confirmation, :persistence_token

  has_many :visualizations
end
