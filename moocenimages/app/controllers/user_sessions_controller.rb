class UserSessionsController < ApplicationController
  def new
    if logged_in?
      redirect_to root_path
    else
      @user_session = UserSession.new
    end
  end

  def create
    @user_session = UserSession.new(params[:user_session])
    if @user_session.save
      redirect_to root_path
    else
      flash[:notice] = "Incorrect username and/or password."
      redirect_to login_path
    end
  end

  def show
    user_session = UserSession.find
    @current_user = user_session.user
  end

  def destroy
    user_session = UserSession.find
    user_session.destroy
    redirect_to :root
  end
end
