class UsersController < ApplicationController
  before_filter :login_required

  def index
    @users = User.find(:all)
  end

  def create
    @user = User.new(params[:user])
    @user.save
  end

  def edit
    @user = current_user
  end

  def update
    @user = current_user
    if @user.update_attributes(params[:user])
      flash[:notice] = "You have sucessfully updated your profile."
    end
    redirect_to users_path
  end

  def destroy
    User.find(params[:id]).destroy
    redirect_to :back
  end
end
