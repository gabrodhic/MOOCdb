require 'test_helper'

class AdminControllerTest < ActionController::TestCase
  test "should get users" do
    get :users
    assert_response :success
  end

  test "should get visualizations" do
    get :visualizations
    assert_response :success
  end

  test "should get offerings" do
    get :offerings
    assert_response :success
  end

end
