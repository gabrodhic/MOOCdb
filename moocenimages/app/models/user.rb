class User < ActiveRecord::Base
  acts_as_authentic
  attr_accessible :username, :email, :crypted_password, :password, :password_confirmation, :is_admin, :persistence_token, :name, :website
end
