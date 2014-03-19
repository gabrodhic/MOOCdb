class ApplicationController < ActionController::Base
  # Prevent CSRF attacks by raising an exception.
  # For APIs, you may want to use :null_session instead.
  protect_from_forgery

  before_filter :configure_permitted_parameters, if: :devise_controller?

  def admin_required
    unless current_user.try(:admin?)
      flash[:notice] = "You must be an admin to do that."
      redirect_to root_path
    end
  end

  def configure_permitted_parameters
    devise_parameter_sanitizer.for(:sign_up) << :email
  end
end
