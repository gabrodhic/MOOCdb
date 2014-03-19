class AdminController < ApplicationController
  before_filter :admin_required

  def users
    if params[:pending]
      @users = User.where(:approved => false)
    else
      @users = User.all
    end
  end

  def approve_user
    user = User.find(params[:user_id])
    user.approved = true
    if user.save
      UserMailer.user_approved(user).deliver
    end

    redirect_to admin_users_path, :pending => true
  end

  def visualizations
  end

  def offerings
  end
end
