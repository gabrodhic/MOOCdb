class ApplicationController < ActionController::Base
  # Prevent CSRF attacks by raising an exception.
  # For APIs, you may want to use :null_session instead.
  protect_from_forgery

  helper_method :current_user_session, :current_user, :logged_in?, :login_required, :admin_required

  private

  def current_user_session
    @current_user_session ||= UserSession.find
  end

  def current_user
    @current_user ||= current_user_session && current_user_session.user
  end

  def logged_in?
  	UserSession.find
  end

  def login_required
    unless logged_in?
      flash[:notice] = "You must be logged in to view that page."
      redirect_to :root
    end
  end
end
