class UsersController < ApplicationController
  before_action :signed_in_user, only: [:index, :edit, :update, :destroy]
  before_action :correct_user, only: [:edit, :update]
  before_action :admin_user, only: [:index, :destroy]

  def home
    if signed_in?
      redirect_to label_path
    else
      redirect_to welcome_path
    end
  end

  def newguest
    if signed_in?
      redirect_to label_path
    end
  end

  def index
    @users = User.paginate(page: params[:page])
  end

  def show
    @user = User.find(params[:id])
  end

  def new
    @user = User.new
  end

  def edit
    @user = User.find(params[:id])
  end

  def update 
    if not params[:user].include?(:current_upload)
      if @user.update_attributes(user_params)
        flash[:success] = "Profile updated"
        redirect_to @user
      else
        render 'edit', location: edit_user_path(@user, :form => "info")
      end
    else
      if @user.update_attribute(:current_upload, project_params[:current_upload])
        @user.clear_current_post
        flash[:success] = "Profile updated"
        redirect_to label_path
      else
        render 'edit'
      end
    end
  end

  def create
    if signed_in?
      flash[:error] = "Please sign out before creating a new account."
      redirect_to current_user
    else
      @user = params[:user] ? User.new(user_params) : User.new_guest
      if @user.save
        sign_in @user
        flash[:success] = "Welcome to #{view_context.full_title('')}"
        redirect_to edit_user_path(@user, :form => "project")
      else
        render 'new'
      end
    end
  end

  def destroy
    User.find(params[:id]).destroy
    flash[:success] = "User deleted."
    redirect_to users_url
  end

  private

    def user_params
      params.require(:user).permit(:name, :email, :password, :password_confirmation, :guest, :current_upload, :tos_agreement)
    end

    def project_params
      params.require(:user).permit(:current_upload)
    end

    def signed_in_user
      unless signed_in?
        store_location
        redirect_to signin_url, notice: "Please sign in."
      end
    end

    def correct_user
      @user = User.find(params[:id])
      redirect_to(root_url) unless current_user?(@user)
    end

    def admin_user
      redirect_to(root_path) unless current_user.admin?
    end
end
